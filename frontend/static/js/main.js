// CarBuy Main JavaScript

// Mobile Navigation Toggle
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });

        // Close mobile menu when clicking on a link
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
            });
        });
    }

    // Update cart count on page load
    updateCartCount();
    
    // Setup add to cart buttons
    setupAddToCartButtons();
});

// Update cart count in navigation
function updateCartCount() {
    fetch('/api/cart_count')
        .then(response => response.json())
        .then(data => {
            const cartCountElement = document.getElementById('cart-count');
            if (cartCountElement) {
                cartCountElement.textContent = data.count || 0;
            }
        })
        .catch(error => {
            console.error('Error updating cart count:', error);
        });
}

// Setup add to cart functionality
function setupAddToCartButtons() {
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', function() {
            const carId = this.getAttribute('data-car-id');
            addToCart(carId);
        });
    });
}

// Add item to cart
function addToCart(carId, quantity = 1) {
    const button = document.querySelector(`[data-car-id="${carId}"]`);
    const originalText = button.innerHTML;
    
    // Show loading state
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Adding...';
    button.disabled = true;
    
    fetch('/api/add_to_cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            car_id: parseInt(carId),
            quantity: quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Show success state
            button.innerHTML = '<i class="fas fa-check"></i> Added!';
            button.classList.add('btn-success');
            button.classList.remove('btn-secondary');
            
            // Update cart count
            updateCartCount();
            
            // Show success message
            showNotification('Item added to cart successfully!', 'success');
            
            // Reset button after 2 seconds
            setTimeout(() => {
                button.innerHTML = originalText;
                button.classList.remove('btn-success');
                button.classList.add('btn-secondary');
                button.disabled = false;
            }, 2000);
        } else {
            // Show error state
            button.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Error';
            button.classList.add('btn-danger');
            button.classList.remove('btn-secondary');
            
            showNotification('Error adding item to cart: ' + data.message, 'error');
            
            // Reset button after 2 seconds
            setTimeout(() => {
                button.innerHTML = originalText;
                button.classList.remove('btn-danger');
                button.classList.add('btn-secondary');
                button.disabled = false;
            }, 2000);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        button.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Error';
        button.classList.add('btn-danger');
        button.classList.remove('btn-secondary');
        
        showNotification('Error adding item to cart', 'error');
        
        // Reset button after 2 seconds
        setTimeout(() => {
            button.innerHTML = originalText;
            button.classList.remove('btn-danger');
            button.classList.add('btn-secondary');
            button.disabled = false;
        }, 2000);
    });
}

// Show notification
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-message">${message}</span>
            <button class="notification-close" onclick="this.parentElement.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    // Add notification styles if not already added
    if (!document.querySelector('#notification-styles')) {
        const style = document.createElement('style');
        style.id = 'notification-styles';
        style.textContent = `
            .notification {
                position: fixed;
                top: 80px;
                right: 20px;
                padding: 1rem 1.5rem;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                z-index: 1001;
                max-width: 400px;
                animation: slideInRight 0.3s ease;
            }
            
            .notification-success {
                background-color: #d4edda;
                color: #155724;
                border-left: 4px solid #28a745;
            }
            
            .notification-error {
                background-color: #f8d7da;
                color: #721c24;
                border-left: 4px solid #dc3545;
            }
            
            .notification-info {
                background-color: #d1ecf1;
                color: #0c5460;
                border-left: 4px solid #17a2b8;
            }
            
            .notification-content {
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 1rem;
            }
            
            .notification-close {
                background: none;
                border: none;
                cursor: pointer;
                opacity: 0.7;
                transition: opacity 0.3s ease;
            }
            
            .notification-close:hover {
                opacity: 1;
            }
            
            @keyframes slideInRight {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            
            @media (max-width: 768px) {
                .notification {
                    right: 10px;
                    left: 10px;
                    max-width: none;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    // Add to page
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add loading animation to buttons
function addLoadingToButton(button, loadingText = 'Loading...') {
    const originalText = button.innerHTML;
    button.innerHTML = `<i class="fas fa-spinner fa-spin"></i> ${loadingText}`;
    button.disabled = true;
    
    return function() {
        button.innerHTML = originalText;
        button.disabled = false;
    };
}

// Format currency (Indonesian Rupiah)
function formatCurrency(amount) {
    return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount);
}

// Debounce function for search/filter inputs
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Handle image loading errors
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('img').forEach(img => {
        img.addEventListener('error', function() {
            // Hide the image and show placeholder
            this.style.display = 'none';
            const placeholder = this.nextElementSibling;
            if (placeholder && placeholder.classList.contains('car-placeholder')) {
                placeholder.style.display = 'flex';
            }
        });
    });
});

// Scroll to top functionality
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Add scroll to top button if page is long enough
window.addEventListener('scroll', function() {
    let scrollTopButton = document.getElementById('scroll-top-btn');
    
    if (window.scrollY > 300) {
        if (!scrollTopButton) {
            scrollTopButton = document.createElement('button');
            scrollTopButton.id = 'scroll-top-btn';
            scrollTopButton.innerHTML = '<i class="fas fa-arrow-up"></i>';
            scrollTopButton.className = 'scroll-top-btn';
            scrollTopButton.onclick = scrollToTop;
            document.body.appendChild(scrollTopButton);
            
            // Add styles for scroll to top button
            if (!document.querySelector('#scroll-top-styles')) {
                const style = document.createElement('style');
                style.id = 'scroll-top-styles';
                style.textContent = `
                    .scroll-top-btn {
                        position: fixed;
                        bottom: 30px;
                        right: 30px;
                        width: 50px;
                        height: 50px;
                        background: linear-gradient(135deg, #e74c3c, #c0392b);
                        color: white;
                        border: none;
                        border-radius: 50%;
                        cursor: pointer;
                        font-size: 1.2rem;
                        box-shadow: 0 4px 12px rgba(231, 76, 60, 0.3);
                        transition: all 0.3s ease;
                        z-index: 1000;
                        animation: fadeInUp 0.3s ease;
                    }
                    
                    .scroll-top-btn:hover {
                        transform: translateY(-3px);
                        box-shadow: 0 6px 20px rgba(231, 76, 60, 0.4);
                    }
                    
                    @keyframes fadeInUp {
                        from {
                            opacity: 0;
                            transform: translateY(20px);
                        }
                        to {
                            opacity: 1;
                            transform: translateY(0);
                        }
                    }
                    
                    @media (max-width: 768px) {
                        .scroll-top-btn {
                            bottom: 20px;
                            right: 20px;
                            width: 45px;
                            height: 45px;
                        }
                    }
                `;
                document.head.appendChild(style);
            }
        }
        scrollTopButton.style.display = 'block';
    } else if (scrollTopButton) {
        scrollTopButton.style.display = 'none';
    }
});