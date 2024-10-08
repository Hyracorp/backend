from rest_framework import generics, status
from rest_framework.response import Response
from django.utils import timezone
from property_management.models import BookVisit
from property_management.serializers import BookVisitSerializer, BookingListSerializer
from django.utils import timezone
from datetime import datetime, timedelta, time
from rest_framework.permissions import IsAuthenticated
from notifications.utils import create_user_notification


class AvailableSlotsAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookVisitSerializer

    def post(self, request, *args, **kwargs):
        date_str = request.data.get('date')
        property_id = request.data.get('property')

        if not date_str:
            return Response({"error": "Date is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not property_id:
            return Response({"error": "Property is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        # Define valid time slots
        valid_slots = ["09:00", "11:00", "13:00", "15:00", "17:00"]

        valid_visit_status = ["Approved", "Pending"]

        # Get booked slots for the given date and property
        booked_slots = BookVisit.objects.filter(
            date=date, property=property_id, visit_status__in=valid_visit_status).values_list('time', flat=True)

        # Current time with timezone support
        now = timezone.localtime(timezone.now())

        # Filter slots that are at least 5 hours in the future
        available_slots = []
        for slot in valid_slots:
            slot_time = datetime.combine(
                date, datetime.strptime(slot, "%H:%M").time())
            slot_time = timezone.make_aware(
                slot_time, timezone.get_current_timezone())

            # Ensure slot is at least 5 hours in the future
            if slot_time - now >= timedelta(hours=5) and slot not in booked_slots:
                # Check if it's after 5 PM today and exclude next day's 9 AM slot
                if now.time() >= time(17, 0) and date == now.date() + timedelta(days=1) and slot == "09:00":
                    continue
                available_slots.append(slot)

        return Response({"date": date_str, "property": property_id, "available_slots": available_slots}, status=status.HTTP_200_OK)


class BookVisitAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookVisitSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, visit_status="Pending")
        create_user_notification(self.request.user, "booking_request",
                                 "Your booking request has been received. Please wait for approval.", '/tenant/bookings')


class BookVisitListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingListSerializer

    def get_queryset(self):
        if (self.request.user.is_superuser):
            return BookVisit.objects.filter(user=self.request.user)
        elif (self.request.user.is_landlord):
            property = self.request.query_params.get('property')
            return BookVisit.objects.filter(property=property)
        elif (self.request.user.is_tenant):
            return BookVisit.objects.filter(user=self.request.user)

        return BookVisit.objects.none()


class UpdateVisitStatusAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = BookVisit.objects.all()
    serializer_class = BookVisitSerializer
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        visit = self.get_object()
        status_to_update = request.data.get('visit_status')
        if not visit:
            return Response({"error": "Visit not found."}, status=status.HTTP_404_NOT_FOUND)

        if not status_to_update or status_to_update not in dict(BookVisit.visit_status_choices):
            return Response({"error": "Invalid visit status."}, status=status.HTTP_400_BAD_REQUEST)

        if request.user != visit.user:
            return Response({"error": "You are not authorized to update this visit."}, status=status.HTTP_403_FORBIDDEN)
        if request.user.is_superuser == False:
            update_choices = ["Cancelled", "Rescheduled"]
            if status_to_update not in update_choices:
                return Response({"error": "You are not authorized to update this visit."}, status=status.HTTP_403_FORBIDDEN)

        if status_to_update == visit.visit_status:
            return Response({"error": "Visit status is already in the desired state."}, status=status.HTTP_400_BAD_REQUEST)

        if status_to_update == "Cancelled" and visit.visit_status != "Pending":
            return Response({"error": "Visit can only be cancelled if it is in Pending status."}, status=status.HTTP_400_BAD_REQUEST)

        # Handle specific status transitions here if needed
        # Example for approval
        if status_to_update == "Approved" and visit.visit_status != "Pending":
            return Response({"error": "Visit can only be approved if it is in Pending status."}, status=status.HTTP_400_BAD_REQUEST)

        visit.visit_status = status_to_update
        visit.save()

        return Response({"status": f"Visit status updated to {status_to_update}."}, status=status.HTTP_200_OK)
