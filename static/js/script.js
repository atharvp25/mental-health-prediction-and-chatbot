// Modern JavaScript with Animations and Interactive Features
document.addEventListener('DOMContentLoaded', function() {
    // Initialize animated background
    createAnimatedBackground();
    
    // Add scroll animations
    initScrollAnimations();
    
    // Add interactive elements
    initInteractiveElements();
    
    // Initialize tooltips
    initTooltips();
});

// Create animated floating bubbles
function createAnimatedBackground() {
    const bgContainer = document.createElement('div');
    bgContainer.className = 'animated-bg';
    document.body.appendChild(bgContainer);

    for (let i = 0; i < 15; i++) {
        const bubble = document.createElement('div');
        bubble.className = 'bubble';
        
        const size = Math.random() * 100 + 50;
        const left = Math.random() * 100;
        const delay = Math.random() * 15;
        const duration = Math.random() * 10 + 15;
        
        bubble.style.width = `${size}px`;
        bubble.style.height = `${size}px`;
        bubble.style.left = `${left}%`;
        bubble.style.animationDelay = `${delay}s`;
        bubble.style.animationDuration = `${duration}s`;
        
        bgContainer.appendChild(bubble);
    }
}

// Initialize scroll animations
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                
                if (entry.target.classList.contains('animate-stagger')) {
                    const children = entry.target.children;
                    Array.from(children).forEach((child, index) => {
                        setTimeout(() => {
                            child.style.opacity = '1';
                            child.style.transform = 'translateY(0)';
                        }, index * 100);
                    });
                }
            }
        });
    }, observerOptions);

    // Observe elements with animation classes
    document.querySelectorAll('.animate-fade-in-up, .animate-slide-left, .animate-slide-right, .animate-stagger').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

// Initialize interactive elements
function initInteractiveElements() {
    // Add ripple effect to buttons
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = button.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = `${size}px`;
            ripple.style.left = `${x}px`;
            ripple.style.top = `${y}px`;
            ripple.className = 'ripple';
            
            const existingRipple = button.querySelector('.ripple');
            if (existingRipple) {
                existingRipple.remove();
            }
            
            button.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });

    // Add CSS for ripple effect
    const rippleStyle = document.createElement('style');
    rippleStyle.textContent = `
        .btn {
            position: relative;
            overflow: hidden;
        }
        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.7);
            transform: scale(0);
            animation: ripple-animation 0.6s linear;
        }
        @keyframes ripple-animation {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(rippleStyle);

    // Add typing effect to hero text
    const heroText = document.querySelector('.hero-text');
    if (heroText) {
        typeWriter(heroText, heroText.textContent, 0);
    }

    // Add counter animation to stats
    animateCounters();
}

// Typewriter effect
function typeWriter(element, text, i) {
    if (i < text.length) {
        element.innerHTML = text.substring(0, i + 1) + '<span class="typing-cursor">|</span>';
        setTimeout(() => typeWriter(element, text, i + 1), 100);
    } else {
        element.innerHTML = text + '<span class="typing-cursor blinking">|</span>';
    }
}

// Animate counter numbers
function animateCounters() {
    const counters = document.querySelectorAll('.counter');
    
    counters.forEach(counter => {
        const target = +counter.getAttribute('data-target');
        const duration = 2000; // 2 seconds
        const step = target / (duration / 16); // 60fps
        
        let current = 0;
        
        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            counter.textContent = Math.floor(current).toLocaleString();
        }, 16);
    });
}

// Initialize tooltips
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Chatbot functionality
function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addMessageToChat(message, 'user');
    input.value = '';
    
    // Show loading indicator
    const loadingId = addLoadingMessage();
    
    // Send to backend
    fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        // Remove loading message
        removeLoadingMessage(loadingId);
        
        // Add bot response
        if (data.response) {
            addMessageToChat(data.response, 'bot');
        }
    })
    .catch(error => {
        removeLoadingMessage(loadingId);
        addMessageToChat('Sorry, I encountered an error. Please try again.', 'bot');
    });
}

function addMessageToChat(message, sender) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    messageDiv.textContent = message;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // Add animation
    messageDiv.style.animation = 'fadeInUp 0.3s ease';
}

function addLoadingMessage() {
    const chatMessages = document.getElementById('chat-messages');
    const loadingDiv = document.createElement('div');
    loadingDiv.id = 'loading-message';
    loadingDiv.className = 'message bot-message';
    loadingDiv.innerHTML = '<div class="loading-spinner"></div> Thinking...';
    
    chatMessages.appendChild(loadingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return 'loading-message';
}

function removeLoadingMessage(id) {
    const loadingMessage = document.getElementById(id);
    if (loadingMessage) {
        loadingMessage.remove();
    }
}

// Enter key support for chat
document.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        const chatInput = document.getElementById('chat-input');
        if (document.activeElement === chatInput) {
            sendMessage();
        }
    }
});

// Score interpretation
function interpretScore(score) {
    if (score >= 80) return { level: 'Excellent', color: 'success', message: 'Your mental health is in great shape!' };
    if (score >= 60) return { level: 'Good', color: 'info', message: 'You\'re doing well overall.' };
    if (score >= 40) return { level: 'Fair', color: 'warning', message: 'There\'s room for improvement.' };
    return { level: 'Needs Attention', color: 'danger', message: 'Consider seeking support.' };
}

// Export functions for global use
window.sendMessage = sendMessage;
window.interpretScore = interpretScore;