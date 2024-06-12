from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from rest_framework import serializers
from .models import NetworkTraffic, AlertNotification
from core.admin import UserCreationForm
from core.models import User, NetworkTraffic
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .seriealizers import NetworkTrafficSerializer
from .emails import (
    send_guess_pass_email, send_smurf_email, send_spy_email, send_ipsweep_email,
    send_neptune_email, send_teardrop_email, send_satan_email
)
from .sms import (
    send_guess_pass_sms, send_smurf_sms, send_spy_sms, send_ipsweep_sms,
    send_neptune_sms, send_teardrop_sms, send_satan_sms
)


# Create your views here.

@login_required
def dashboard_view(request):
    dt = timezone.now()
    today = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    context = {
        'user': request.user,
        'network_logs': NetworkTraffic.objects.all()[:5],
        'user_no': User.objects.all().count(),
        'total_logs': NetworkTraffic.objects.all().count(),
        'today_logs': NetworkTraffic.objects.filter(created_at__gte=today).count(),
        'sum_normal': NetworkTraffic.objects.filter(outcome='normal').count(),
        'sum_pass': NetworkTraffic.objects.filter(outcome='guess_passwd').count(),
        'sum_smurf': NetworkTraffic.objects.filter(outcome='smurf').count(),
        'sum_neptune': NetworkTraffic.objects.filter(outcome='neptune').count(),
        'sum_tear_drop': NetworkTraffic.objects.filter(outcome='teardrop').count(),
        'sum_port_sweep': NetworkTraffic.objects.filter(outcome='portsweep').count(),
        'sum_tcp': NetworkTraffic.objects.filter(protocol_type='tcp').count(),
        'sum_udp': NetworkTraffic.objects.filter(protocol_type='udp').count(),
        'sum_http': NetworkTraffic.objects.filter(service='http').count(),
        'sum_icmp': NetworkTraffic.objects.filter(protocol_type='icmp').count() ,
        'sum_smtp': NetworkTraffic.objects.filter(service='smtp').count(),
        'sum_domain': NetworkTraffic.objects.filter(service='domain').count(),
        'sum_ftp': NetworkTraffic.objects.filter(service='ftp').count(),
        'sum_ssh': NetworkTraffic.objects.filter(service='ssh').count(),
        'sum_telnet': NetworkTraffic.objects.filter(service='telnet').count(),
        'sum_private': NetworkTraffic.objects.filter(service='private').count(),

    }
    return render(request, 'index.html', context)


@login_required
def logs_view(request):
    context = {
        'network_logs': NetworkTraffic.objects.all()
    }
    return render(request, 'logs.html', context)


@login_required
def users_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                email=form.data['email'],
                first_name=form.data['first_name'],
                last_name=form.data['last_name'],
                password=form.data['password1'],
                cell=form.data['cell']
            )
            user.save()
            return redirect('users')
        else:
            messages.error(request, form.errors)
    else:
        form = UserCreationForm()

    context = {
        'users': User.objects.all(),
        'form': UserCreationForm()
    }
    return render(request, 'users.html', context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('dashboard')


# Function to save Alert to DB

def save_notification(outcome, protocol, service):
    alert = AlertNotification.objects.create(
        outcome=outcome,
        service=service,
        protocol_type=protocol
    )
    alert.save()


@api_view(['POST'])
def upload_network_log(request):
    if request.method == 'POST':
        data = request.data

        # Custom processing logic
        if 'src_bytes' not in data:
            data['src_bytes'] = 0  # Default value if not provided
        if 'dst_bytes' not in data:
            data['dst_bytes'] = 0  # Default value if not provided
        if 'outcome' not in data:
            data['outcome'] = 'unknown'  # Default outcome if not provided

        # Additional custom logic can be added here

        serializer = NetworkTrafficSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            # Determine the type of alert to send based on outcome
            outcome = data.get('outcome')
            protocol_type = data.get('protocol_type')
            service = data.get('service')
            if outcome == 'guess_passwd':
                send_guess_pass_email()
                send_guess_pass_sms()
                save_notification(outcome, protocol_type, service)
            elif outcome == 'smurf':
                send_smurf_email()
                send_smurf_sms()
                save_notification(outcome, protocol_type, service)
            elif outcome == 'spy':
                send_spy_email()
                send_spy_sms()
                save_notification(outcome, protocol_type, service)
            elif outcome == 'ipsweep':
                send_ipsweep_email()
                send_ipsweep_sms()
                save_notification(outcome, protocol_type, service)
            elif outcome == 'neptune':
                send_neptune_email()
                send_neptune_sms()
                save_notification(outcome, protocol_type, service)
            elif outcome == 'teardrop':
                send_teardrop_email()
                send_teardrop_sms()
                save_notification(outcome, protocol_type, service)
            elif outcome == 'satan':
                send_satan_email()
                send_satan_sms()
                save_notification(outcome, protocol_type, service)

            # Send data to WebSocket
            dt = timezone.now()
            today = dt.replace(hour=0, minute=0, second=0, microsecond=0)
            channel_layer = get_channel_layer()
            data = {
                'total_logs': NetworkTraffic.objects.all().count(),
                'today_logs': NetworkTraffic.objects.filter(created_at__gte=today).count(),
                'sum_normal': NetworkTraffic.objects.filter(outcome='normal').count(),
                'sum_pass': NetworkTraffic.objects.filter(outcome='guess_passwd').count(),
                'sum_smurf': NetworkTraffic.objects.filter(outcome='smurf').count(),
                'sum_neptune': NetworkTraffic.objects.filter(outcome='neptune').count(),
                'sum_tear_drop': NetworkTraffic.objects.filter(outcome='teardrop').count(),
                'sum_port_sweep': NetworkTraffic.objects.filter(outcome='portsweep').count(),
                'sum_tcp': NetworkTraffic.objects.filter(protocol_type='tcp').count(),
                'sum_udp': NetworkTraffic.objects.filter(protocol_type='udp').count(),
                'sum_http': NetworkTraffic.objects.filter(service='http').count(),
                'sum_icmp': NetworkTraffic.objects.filter(protocol_type='icmp').count(),
                'sum_smtp': NetworkTraffic.objects.filter(service='smtp').count(),
                'sum_domain': NetworkTraffic.objects.filter(service='domain').count(),
                'sum_ftp': NetworkTraffic.objects.filter(service='ftp').count(),
                'sum_ssh': NetworkTraffic.objects.filter(service='ssh').count(),
                'sum_telnet': NetworkTraffic.objects.filter(service='telnet').count(),
                'sum_private': NetworkTraffic.objects.filter(service='private').count(),
            }
            async_to_sync(channel_layer.group_send)(
                "network_logs",
                {
                    "type": "send_log",
                    "log": data
                }
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def alert_view(request):
    context = {
        'alerts': AlertNotification.objects.all()
    }
    return render(request, 'alerts.html', context)
