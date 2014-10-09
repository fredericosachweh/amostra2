import datetime

from django.test import TransactionTestCase

from clients import factories
from clients import models


class UnitTestCase(TransactionTestCase):
    fixtures = (
        'auth_groups.json',
    )

    def setUp(self):
        self.client = factories.ClientFactory.create()
        self.user = factories.UserFactory.create()

    def reload_client(self):
        self.client = models.Client.objects.get(pk=self.client.pk)

    def test_manager_get_proper_group(self):
        """
        Tests that attaching a user to a client as manager adds it to the
        managers group.
        """
        # the user aren't a manager yet
        assert 'managers' not in self.user.groups.values_list('name', flat=True)
        # but, when add it as manager to any client
        self.client.managers.add(self.user)
        # it got added to the managers group automatically
        assert 'managers' in self.user.groups.values_list('name', flat=True)

    def test_teacher_get_proper_group(self):
        """
        Tests that attaching a user to a client as teacher adds it to the
        teachers group.
        """
        # the user aren't a manager yet
        assert 'teachers' not in self.user.groups.values_list('name', flat=True)
        # but, when add it as manager to any client
        models.Teacher.objects.create(client=self.client, teacher=self.user)
        # it got added to the managers group automatically
        assert 'teachers' in self.user.groups.values_list('name', flat=True)

    def test_client_status_change_log(self):
        """
        Tests that there will be a new follow up entry logging the client
        status change.
        """
        self.assertEqual(self.client.status, 'suspect')
        self.assertEqual(self.client.followup_set.count(), 0)

        self.client.status = 'prospect'
        self.client.save()

        self.assertEqual(self.client.followup_set.count(), 1)
        fw = self.client.followup_set.get()

        self.assertIn('suspect para prospect', fw.content)

    def test_contract_status(self):
        """
        Tests that a payment changes the contract status.
        """
        future_date = datetime.datetime.now() + datetime.timedelta(days=7)
        contract = self.client.contract_set.create(document='1234')
        klass = contract.klass_set.create(name='Test class',
                                          end_date=future_date)

        payment = contract.payment_set.create(due_date=future_date)
        payment.klasspayment_set.create(klass=klass)

        contract = self.client.contract_set.get()
        self.assertTrue(contract.pending_payment)

        payment.payment_date = datetime.datetime.now()
        payment.save()

        contract = self.client.contract_set.get()
        self.assertTrue(payment.was_paid)
        self.assertFalse(contract.pending_payment)

    def test_client_status(self):
        """
        Tests different possibilities for the client status.

        The client status is denormalized and depends of various environment
        conditions. It is saved and explained in the `clients.status` module.
        It is also covered in the clients docs section.
        """
        current_date = datetime.datetime.now()
        future_date = current_date + datetime.timedelta(days=7)
        past_date = current_date - datetime.timedelta(days=40)  # force another month

        # Start at suspect
        self.assertEqual(self.client.status, 'suspect')

        # A task sets a client as a prospect
        self.client.followup_set.create(content='Sample task',
                                        due_date=future_date,
                                        responsible=self.user)
        self.reload_client()
        self.assertEqual(self.client.status, 'prospect')

        # The lack of it makes the client be a suspect again
        self.client.followup_set.all().delete()
        self.reload_client()
        self.assertEqual(self.client.status, 'suspect')

        # A demonstration also sets a client as a prospect
        self.client.demonstration_set.create(valid_until=future_date)
        self.reload_client()
        self.assertEqual(self.client.status, 'prospect')

        # A klass doesn't affect client status until there is a payment
        contract = self.client.contract_set.create(document='1234')
        klass = contract.klass_set.create(name='Test class',
                                          end_date=future_date)
        self.reload_client()
        self.assertEqual(self.client.status, 'prospect')

        # A client will be a lead when there is only one payment
        payment = contract.payment_set.create(due_date=future_date)
        payment.klasspayment_set.create(klass=klass)
        self.reload_client()
        self.assertEqual(self.client.status, 'lead')

        # An up-to-date client has status client
        payment.payment_date = datetime.datetime.now()
        payment.save()
        self.reload_client()
        self.assertTrue(payment.was_paid)
        self.assertEqual(self.client.status, 'active')

        # Removes all the payments for any reason brings back to prospect
        payment.delete()
        self.reload_client()
        self.assertTrue(self.client.status, 'prospect')

        # More than one payment, with one of them pending, will make the client
        # frozen (e.g. has unacessible klasses)
        paid_payment = contract.payment_set.create(due_date=past_date,
                                                   payment_date=past_date)
        paid_payment.klasspayment_set.create(klass=klass)
        pending_payment = contract.payment_set.create(due_date=future_date)
        pending_payment.klasspayment_set.create(klass=klass)
        self.reload_client()
        self.assertTrue(self.client.status, 'frozen')

        # But when the pending payment is paid, the client becomes active again
        pending_payment.payment_date = future_date
        pending_payment.save()
        self.reload_client()
        self.assertTrue(self.client.status, 'active')

    def test_late_klasses(self):
        """
        Tests when a klass is blocked due late payment.
        """
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        contract = self.client.contract_set.create(document='1234')
        klass = contract.klass_set.create(name='Test class',
                                          end_date=tomorrow)
        payment = contract.payment_set.create(due_date=tomorrow)
        payment.klasspayment_set.create(klass=klass)

        # Only one pending payment makes the klass pending
        self.assertFalse(payment.was_paid)
        self.assertEqual(contract.klass_set.late_payment().count(), 1)

        # Pay the only one klass payment makes the klass active
        payment.payment_date = tomorrow
        payment.save()
        self.assertEqual(contract.klass_set.late_payment().count(), 0)

    def test_contract_unique_document(self):
        """
        Tests that the contract's document is unique.

        If I create a contract A with the document number 123 and try to create
        a new contract B with the same number 123, I will get an error.
        """
        contract_a = self.client.contract_set.create(document='123')
        with self.assertRaises(ValueError):
            contract_b = self.client.contract_set.create(document='123')
        self.assertEqual(self.client.contract_set.count(), 1)
