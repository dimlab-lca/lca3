document.addEventListener('DOMContentLoaded', function() {
    // Add fade-in animation to elements
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '0';
                entry.target.style.transform = 'translateY(20px)';
                entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
            }
        });
    }, observerOptions);

    // Observe all video cards
    document.querySelectorAll('.video-card').forEach(card => {
        observer.observe(card);
    });

    // Create and handle "Go to top" button
    const fabTop = document.createElement('button');
    fabTop.className = 'fab-top';
    fabTop.innerHTML = '<i class="fas fa-arrow-up"></i>';
    fabTop.title = 'Retour en haut';
    fabTop.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #2d8f5f 0%, #1e6091 100%);
        color: white;
        border: none;
        border-radius: 50%;
        font-size: 1.5rem;
        cursor: pointer;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        opacity: 0;
        transform: translateY(100px);
        z-index: 1000;
    `;
    document.body.appendChild(fabTop);

    // Show/hide fab button based on scroll position
    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            fabTop.style.opacity = '1';
            fabTop.style.transform = 'translateY(0)';
        } else {
            fabTop.style.opacity = '0';
            fabTop.style.transform = 'translateY(100px)';
        }
    });

    // Smooth scroll to top
    fabTop.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // Enhanced video card hover effects
    document.querySelectorAll('.video-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Category filter active state management
    const categoryBtns = document.querySelectorAll('.category-btn');
    categoryBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            categoryBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // Mobile menu functionality
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const nav = document.querySelector('.nav');
    
    if (mobileMenuBtn && nav) {
        mobileMenuBtn.addEventListener('click', function() {
            if (nav.style.display === 'flex') {
                nav.style.display = 'none';
            } else {
                nav.style.display = 'flex';
                nav.style.flexDirection = 'column';
                nav.style.position = 'absolute';
                nav.style.top = '100%';
                nav.style.left = '0';
                nav.style.right = '0';
                nav.style.background = 'linear-gradient(135deg, #2d8f5f 0%, #1e6091 100%)';
                nav.style.padding = '1rem';
                nav.style.boxShadow = '0 4px 20px rgba(0,0,0,0.1)';
            }
        });
    }

    // Add CSS animations
    const style = document.createElement('style');
    style.textContent = `
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
        
        .fab-top:hover {
            transform: scale(1.1) !important;
            box-shadow: 0 8px 25px rgba(0,0,0,0.3) !important;
        }
    `;
    document.head.appendChild(style);
});