from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message
from properties.models import Property
from django.db.models import Q

@login_required
def start_conversation(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id)
    seller = property_obj.owner
    
    if seller == request.user:
        return redirect('properties:property_detail', slug=property_obj.slug)
    
    # Check if conversation already exists for this property between these users
    conversation = Conversation.objects.filter(property=property_obj, participants=request.user).filter(participants=seller).first()
    
    if not conversation:
        conversation = Conversation.objects.create(property=property_obj)
        conversation.participants.add(request.user, seller)
    
    return redirect('conversations:chat_detail', conversation_id=conversation.id)

@login_required
def chat_list(request):
    conversations = request.user.conversations.all()
    return render(request, 'conversations/chat_list.html', {'conversations': conversations})

@login_required
def chat_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    messages = conversation.messages.all()
    
    # Mark messages as read
    messages.exclude(sender=request.user).update(is_read=True)
    
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                text=text
            )
            conversation.save() # Update updated_at
            return redirect('conversations:chat_detail', conversation_id=conversation.id)
            
    return render(request, 'conversations/chat_detail.html', {
        'conversation': conversation,
        'messages': messages
    })
