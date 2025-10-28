import json

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase


from .implementation.models import (
    Client,
    NextOfKin,
    LoanApplication
)

User = get_user_model()


class APILoanApplicationModuleModelsTests(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.agent = User.objects.create_user(
            username="agent1",
            email="agent1@gmail.com",
            is_agent=True,
            password="secret"
        )
        cls.client_instance = Client.objects.create(
            first_name="client1",
            last_name="test",
            national_id="12-34567A89",
            accepted_terms=True,
            created_by=cls.agent
        )
        cls.next_of_kin = NextOfKin.objects.create(
            client=cls.client_instance,
            name="client1's mother",
            relationship="mother",
            contact="+263 77 899 9999",
            address="test address"
        )
        cls.loan_application = LoanApplication.objects.create(
            client=cls.client_instance,
            amount_requested=10000.0,
            term_months=48,
            loan_purpose="buy company assets",
            submitted_by=cls.agent
        )

    def setUp(self):
        self.client.force_login(user=self.agent)

    def test_client_model(self):
        self.assertEqual(getattr(self.client_instance, "created_by"), self.agent)
        self.assertEqual(getattr(self.client_instance, "national_id"), "12-34567A89")
        self.assertTrue(getattr(self.client_instance, "accepted_terms"))
    
    def test_next_of_kin_model(self):
        self.assertEqual(getattr(self.next_of_kin, "client"), self.client_instance)
        self.assertEqual(getattr(self.next_of_kin, "name"), "client1's mother")
        self.assertEqual(getattr(self.next_of_kin, "relationship"), "mother")
        self.assertEqual(getattr(self.next_of_kin, "address"), "test address")
    
    def test_loan_application_model(self):
        self.assertEqual(getattr(self.loan_application, "client"), self.client_instance)
        self.assertEqual(getattr(self.loan_application, "amount_requested"), 10000)
        self.assertEqual(getattr(self.loan_application, "term_months"), 48)
        self.assertEqual(getattr(self.loan_application, "loan_purpose"), "buy company assets")
        self.assertEqual(getattr(self.loan_application, "submitted_by"), self.agent)


class ClientListCreateViewTests(APITestCase):
    def setUp(self):
        self.agent = User.objects.create_user(
            username="agent1",
            email="agent1@gmail.com",
            is_agent=True,
            password="secret"
        )
        self.client.force_authenticate(user=self.agent)
        self.list_url = reverse("agent-clients")

    def test_agent_can_create_client(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "national_id": "12-345678Z12"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.count(), 1)
        self.assertEqual(Client.objects.first().created_by, self.agent)

    def test_agent_can_list_only_their_clients(self):
        Client.objects.create(first_name="Jane", last_name="Smith", national_id="11-111111Z11", created_by=self.agent)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class ClientDetailViewTests(APITestCase):
    def setUp(self):
        self.agent = User.objects.create_user(
            username="agent1",
            email="agent1@gmail.com",
            is_agent=True,
            password="secret"
        )
        self.client.force_authenticate(user=self.agent)
        self.client_obj = Client.objects.create(first_name="John", last_name="Doe", national_id="12-345678Z12", created_by=self.agent)
        self.detail_url = reverse("client-detail", args=[self.client_obj.pk])

    def test_agent_can_retrieve_client(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "John")

    def test_agent_cannot_update_client(self):
        data = {"first_name": "Updated"}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client_obj.refresh_from_db()
        self.assertNotEqual(self.client_obj.first_name, "Updated")
        self.assertEqual(self.client_obj.first_name, "John")

    def test_agent_cannot_delete_client(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Client.objects.exists())


class NextOfKinViewTests(APITestCase):
    def setUp(self):
        self.agent = User.objects.create_user(
            username="agent1",
            email="agent1@gmail.com",
            is_agent=True,
            password="secret"
        )
        self.client.force_authenticate(user=self.agent)
        self.client_obj = Client.objects.create(first_name="John", last_name="Doe", national_id="12-345678Z12", created_by=self.agent)
        self.list_url = reverse("client-next-of-kin", args=[self.client_obj.pk])

    def test_create_next_of_kin(self):
        data = {
            "name": "Jane Doe",
            "relationship": "Sister",
            "contact": "+263777777777",
            "address": "123 Street"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NextOfKin.objects.count(), 1)

    def test_list_next_of_kin_for_client(self):
        NextOfKin.objects.create(client=self.client_obj, name="Jane Doe", relationship="Sister", contact="+263777777777", address="123 Street")
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class LoanApplicationViewTests(APITestCase):
    def setUp(self):
        self.agent = User.objects.create_user(username="agent1", password="testpass")
        self.client.force_authenticate(user=self.agent)
        self.client_obj = Client.objects.create(first_name="John", last_name="Doe", national_id="12-345678Z12", created_by=self.agent)
        self.list_url = reverse("client-loan", args=[self.client_obj.pk])

    def test_create_loan_application(self):
        data = {
            "amount_requested": 500,
            "term_months": 6,
            "loan_purpose": "Business",
            "daily_repayment": 100,
            "interest_rate": 10,
            "interest_amount": 50,
            "total_payable": 550
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LoanApplication.objects.count(), 1)

    def test_list_loan_applications_for_client(self):
        LoanApplication.objects.create(client=self.client_obj, amount_requested=500, term_months=6, loan_purpose="Business", daily_repayment=100, interest_rate=10, interest_amount=50, total_payable=550, submitted_by=self.agent)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
