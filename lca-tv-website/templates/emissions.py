#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 22:13:11 2025

@author: tmsa
"""

{% extends "base.html" %}

{% block title %}Émissions & Magazines - LCA TV{% endblock %}

{% block content %}
<div style="display: grid; grid-template-columns: 1fr 350px; gap: 30px; margin-top: 0;">
    <div class="content-left">
        <h1 style="font-size: 32px; color: #28a745; margin-bottom: 10px; text-align: center;">Émissions & Magazines</h1>
        <p style="color: #666; margin-bottom: 30px; text-align: center; font-size: 16px;">Découvrez nos programmes phares et magazines spécialisés</p>
        
        <!-- Categories Filter -->
        <div style="display: flex; flex-wrap: wrap; gap: 15px; margin-bottom: 30px; justify-content: center;">
            <a href="#" class="category-filter active" data-category="all" style="background: #28a745; color: white; padding: 10px 20px; border-radius: 25px; text-decoration: none; font-weight: 600; transition: all 0.3s ease;">
                <i class="fas fa-th"></i> Toutes
            </a>
            <a href="#" class="category-filter" data-category="debats" style="background: white; border: 2px solid #28a745; color: #28a745; padding: 10px 20px; border-radius: 25px; text-decoration: none; font-weight: 600; transition: all 0.3s ease;">
                <i class="fas fa-comments"></i> Débats
            </a>
            <a href="#" class="category-filter" data-category="culture" style="background: white; border: 2px solid #28a745; color: #28a745; padding: 10px 20px; border-radius: 25px; text-decoration: none; font-weight: 600; transition: all 0.3s ease;">
                <i class="fas fa-mask"></i> Culture
            </a>
            <a href="#" class="category-filter" data-category="sport" style="background: white; border: 2px solid #28a745; color: #28a745; padding: 10px 20px; border-radius: 25px; text-decoration: none; font-weight: 600; transition: all 0.3s ease;">
                <i class="fas fa-futbol"></i> Sport
            </a>
            <a href="#" class="category-filter" data-category="societe" style="background: white; border: 2px solid #28a745; color: #28a745; padding: 10px 20px; border-radius: 25px; text-decoration: none; font-weight: 600; transition: all 0.3s ease;">
                <i class="fas fa-users"></i> Société
            </a>
        </div>

        <!-- Featured Shows -->
        <div style="margin-bottom: 50px;">
            <h2 style="font-size: 1.8rem; color: #333; margin-bottom: 25px; font-weight: bold; display: flex; align-items: center; gap: 10px;">
                <i class="fas fa-star" style="color: #e74c3c;"></i>
                Émissions Phares
            </h2>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 25px; margin-bottom: 30px;">
                <!-- Franc Parler -->
                <div class="show-card" data-category="debats" style="background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.1); transition: transform 0.3s ease; cursor: pointer;" onclick="playVideo('dQw4w9WgXcQ')">
                    <div style="position: relative; height: 200px; background: linear-gradient(135deg, #e74c3c, #c0392b); overflow: hidden;">
                        <img src="https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg" style="width: 100%; height: 100%; object-fit: cover; opacity: 0.7;">
                        <div style="position: absolute; inset: 0; background: linear-gradient(45deg, rgba(231,76,60,0.8), rgba(192,57,43,0.6));"></div>
                        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; color: white;">
                            <div style="width: 60px; height: 60px; background: rgba(255,255,255,0.2); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; font-size: 1.5rem;">
                                <i class="fas fa-play"></i>
                            </div>
                            <div style="font-weight: bold; font-size: 1.1rem;">REGARDER</div>
                        </div>
                        <div style="position: absolute; top: 15px; left: 15px; background: #28a745; padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; color: white;">
                            DÉBAT
                        </div>
                        <div style="position: absolute; top: 15px; right: 15px; background: rgba(0,0,0,0.6); padding: 6px 12px; border-radius: 20px; font-size: 12px; color: white;">
                            <i class="fas fa-eye"></i> 15.2K
                        </div>
                    </div>
                    <div style="padding: 20px;">
                        <h3 style="font-size: 1.3rem; font-weight: bold; color: #333; margin-bottom: 10px;">Franc Parler</h3>
                        <p style="color: #666; font-size: 0.95rem; line-height: 1.5; margin-bottom: 15px;">Le rendez-vous quotidien du débat politique et social au Burkina Faso. Des discussions franches sur les enjeux de société.</p>
                        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.85rem; color: #888;">
                            <span><i class="fas fa-clock"></i> Lundi - Vendredi 14h30</span>
                            <span style="background: #e74c3c; color: white; padding: 4px 10px; border-radius: 12px; font-weight: bold;">EN DIRECT</span>
                        </div>
                    </div>
                </div>

                <!-- Soleil d'Afrique -->
                <div class="show-card" data-category="culture" style="background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.1); transition: transform 0.3s ease; cursor: pointer;" onclick="playVideo('Xce8DNW7CEg')">
                    <div style="position: relative; height: 200px; background: linear-gradient(135deg, #f39c12, #e67e22); overflow: hidden;">
                        <img src="https://i.ytimg.com/vi/Xce8DNW7CEg/hqdefault.jpg" style="width: 100%; height: 100%; object-fit: cover; opacity: 0.7;">
                        <div style="position: absolute; inset: 0; background: linear-gradient(45deg, rgba(243,156,18,0.8), rgba(230,126,34,0.6));"></div>
                        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; color: white;">
                            <div style="width: 60px; height: 60px; background: rgba(255,255,255,0.2); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; font-size: 1.5rem;">
                                <i class="fas fa-play"></i>
                            </div>
                            <div style="font-weight: bold; font-size: 1.1rem;">REGARDER</div>
                        </div>
                        <div style="position: absolute; top: 15px; left: 15px; background: #f39c12; padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; color: white;">
                            CULTURE
                        </div>
                        <div style="position: absolute; top: 15px; right: 15px; background: rgba(0,0,0,0.6); padding: 6px 12px; border-radius: 20px; font-size: 12px; color: white;">
                            <i class="fas fa-eye"></i> 8.7K
                        </div>
                    </div>
                    <div style="padding: 20px;">
                        <h3 style="font-size: 1.3rem; font-weight: bold; color: #333; margin-bottom: 10px;">Soleil d'Afrique</h3>
                        <p style="color: #666; font-size: 0.95rem; line-height: 1.5; margin-bottom: 15px;">Magazine culturel hebdomadaire célébrant la richesse artistique et patrimoniale du continent africain.</p>
                        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.85rem; color: #888;">
                            <span><i class="fas fa-clock"></i> Dimanche 15h00</span>
                            <span style="background: #f39c12; color: white; padding: 4px 10px; border-radius: 12px; font-weight: bold;">HEBDO</span>
                        </div>
                    </div>
                </div>

                <!-- 7 Afrique -->
                <div class="show-card" data-category="societe" style="background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.1); transition: transform 0.3s ease; cursor: pointer;" onclick="playVideo('3tmd-ClpJxA')">
                    <div style="position: relative; height: 200px; background: linear-gradient(135deg, #4472c4, #3451a3); overflow: hidden;">
                        <img src="https://i.ytimg.com/vi/3tmd-ClpJxA/hqdefault.jpg" style="width: 100%; height: 100%; object-fit: cover; opacity: 0.7;">
                        <div style="position: absolute; inset: 0; background: linear-gradient(45deg, rgba(68,114,196,0.8), rgba(52,81,163,0.6));"></div>
                        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; color: white;">
                            <div style="width: 60px; height: 60px; background: rgba(255,255,255,0.2); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; font-size: 1.5rem;">
                                <i class="fas fa-play"></i>
                            </div>
                            <div style="font-weight: bold; font-size: 1.1rem;">REGARDER</div>
                        </div>
                        <div style="position: absolute; top: 15px; left: 15px; background: #4472c4; padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; color: white;">
                            MAGAZINE
                        </div>
                        <div style="position: absolute; top: 15px; right: 15px; background: rgba(0,0,0,0.6); padding: 6px 12px; border-radius: 20px; font-size: 12px; color: white;">
                            <i class="fas fa-eye"></i> 12.5K
                        </div>
                    </div>
                    <div style="padding: 20px;">
                        <h3 style="font-size: 1.3rem; font-weight: bold; color: #333; margin-bottom: 10px;">7 Afrique</h3>
                        <p style="color: #666; font-size: 0.95rem; line-height: 1.5; margin-bottom: 15px;">Magazine d'actualité panafricaine explorant les enjeux sociétaux, économiques et politiques du continent.</p>
                        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.85rem; color: #888;">
                            <span><i class="fas fa-clock"></i> Samedi 19h00</span>
                            <span style="background: #4472c4; color: white; padding: 4px 10px; border-radius: 12px; font-weight: bold;">PREMIUM</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Publicité Banner -->
        <div style="background: linear-gradient(135deg, #f8f9fa, #e9ecef); border-radius: 15px; padding: 30px; margin-bottom: 40px; text-align: center; border: 2px dashed #dee2e6;">
            <h3 style="color: #666; margin-bottom: 15px; font-size: 1.1rem;">ESPACE PUBLICITAIRE PREMIUM</h3>
            <div style="height: 150px; background: white; border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                <div style="text-align: center; color: #adb5bd;">
                    <i class="fas fa-bullhorn" style="font-size: 2.5rem; margin-bottom: 10px;"></i>
                    <div style="font-size: 1.1rem; font-weight: 600;">Votre publicité ici</div>
                    <div style="font-size: 0.9rem;">728 x 150 pixels</div>
                </div>
            </div>
        </div>

        <!-- All Shows Grid -->
        <div style="margin-bottom: 40px;">
            <h2 style="font-size: 1.8rem; color: #333; margin-bottom: 25px; font-weight: bold; display: flex; align-items: center; gap: 10px;">
                <i class="fas fa-tv" style="color: #4472c4;"></i>
                Toutes nos Émissions
            </h2>
            
            <div id="shows-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px;">
                {% for video in videos %}
                <div class="emission-card" data-category="{{ video.category }}" style="background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 8px 25px rgba(0,0,0,0.1); transition: transform 0.3s ease; cursor: pointer;" data-video-id="{{ video.id }}">
                    <div style="position: relative; height: 160px; overflow: hidden;">
                        <img src="{{ video.thumbnail }}" style="width: 100%; height: 100%; object-fit: cover;">
                        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 45px; height: 45px; background: rgba(231, 76, 60, 0.9); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 1.1rem; opacity: 0; transition: opacity 0.3s ease;">
                            <i class="fas fa-play"></i>
                        </div>
                        <div style="position: absolute; top: 10px; left: 10px; background: #28a745; color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px; font-weight: bold; text-transform: uppercase;">
                            {{ video.category }}
                        </div>
                    </div>
                    <div style="padding: 15px;">
                        <h3 style="font-size: 1rem; font-weight: bold; color: #333; margin-bottom: 8px; line-height: 1.3;">{{ video.title[:60] }}{% if video.title|length > 60 %}...{% endif %}</h3>
                        <p style="color: #666; font-size: 0.85rem; line-height: 1.4; margin-bottom: 12px;">{{ video.description[:90] }}{% if video.description|length > 90 %}...{% endif %}</p>
                        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.75rem; color: #888;">
                            <span><i class="fas fa-calendar"></i> {{ video.published_at[:10] }}</span>
                            <span><i class="fas fa-clock"></i> 25 min</span>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>

    <div class="sidebar">
        <!-- Programme du Jour -->
        <div style="background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 8px 25px rgba(0,0,0,0.1); margin-bottom: 25px;">
            <h3 style="background: #28a745; color: white; padding: 15px 20px; margin: 0; font-size: 16px; display: flex; align-items: center; gap: 10px;">
                <i class="fas fa-calendar-day"></i>
                Programme du Jour
            </h3>
            <div style="padding: 20px;">
                <div style="margin-bottom: 15px; padding-bottom: 15px; border-bottom: 1px solid #eee;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="background: #e74c3c; color: white; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: bold;">14:30</span>
                        <span style="color: #e74c3c; font-size: 12px; font-weight: bold;">● LIVE</span>
                    </div>
                    <h4 style="color: #333; font-size: 0.95rem; margin-bottom: 5px;">Franc Parler</h4>
                    <p style="color: #666; font-size: 0.8rem;">Débat politique quotidien</p>
                </div>

                <div style="margin-bottom: 15px; padding-bottom: 15px; border-bottom: 1px solid #eee;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="background: #f39c12; color: white; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: bold;">15:00</span>
                        <span style="color: #666; font-size: 12px;">REDIFF</span>
                    </div>
                    <h4 style="color: #333; font-size: 0.95rem; margin-bottom: 5px;">Soleil d'Afrique</h4>
                    <p style="color: #666; font-size: 0.8rem;">Magazine culturel</p>
                </div>

                <div style="margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="background: #4472c4; color: white; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: bold;">19:00</span>
                        <span style="color: #4472c4; font-size: 12px; font-weight: bold;">NOUVEAU</span>
                    </div>
                    <h4 style="color: #333; font-size: 0.95rem; margin-bottom: 5px;">7 Afrique</h4>
                    <p style="color: #666; font-size: 0.8rem;">Magazine panafricain</p>
                </div>
            </div>
        </div>

        <!-- Publicité Sidebar -->
        <div style="background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 8px 25px rgba(0,0,0,0.1); margin-bottom: 25px;">
            <div style="background: #4472c4; color: white; padding: 10px 15px; text-align: center; font-size: 12px; font-weight: bold;">
                PUBLICITÉ
            </div>
            <div style="height: 250px; background: linear-gradient(135deg, #f8f9fa, #e9ecef); display: flex; align-items: center; justify-content: center;">
                <div style="text-align: center; color: #6c757d;">
                    <i class="fas fa-ad" style="font-size: 2rem; margin-bottom: 10px;"></i>
                    <div style="font-weight: 600;">Espace Pub</div>
                    <div style="font-size: 0.8rem;">300 x 250</div>
                </div>
            </div>
        </div>

        <!-- Émissions Populaires -->
        <div style="background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 8px 25px rgba(0,0,0,0.1); margin-bottom: 25px;">
            <h3 style="background: #e74c3c; color: white; padding: 15px 20px; margin: 0; font-size: 16px; display: flex; align-items: center; gap: 10px;">
                <i class="fas fa-fire"></i>
                Tendances
            </h3>
            <div style="padding: 20px;">
                <div style="margin-bottom: 15px; display: flex; gap: 10px; cursor: pointer;" onclick="playVideo('dQw4w9WgXcQ')">
                    <div style="width: 60px; height: 45px; background: #e74c3c; border-radius: 6px; display: flex; align-items: center; justify-content: center; color: white; font-size: 0.8rem;">
                        <i class="fas fa-play"></i>
                    </div>
                    <div style="flex: 1;">
                        <h5 style="color: #333; font-size: 0.85rem; margin-bottom: 3px; line-height: 1.2;">Question de Femme</h5>
                        <p style="color: #666; font-size: 0.75rem; margin: 0;">15.2K vues</p>
                    </div>
                </div>

                <div style="margin-bottom: 15px; display: flex; gap: 10px; cursor: pointer;" onclick="playVideo('Xce8DNW7CEg')">
                    <div style="width: 60px; height: 45px; background: #f39c12; border-radius: 6px; display: flex; align-items: center; justify-content: center; color: white; font-size: 0.8rem;">
                        <i class="fas fa-play"></i>
                    </div>
                    <div style="flex: 1;">
                        <h5 style="color: #333; font-size: 0.85rem; margin-bottom: 3px; line-height: 1.2;">Hits Africains</h5>
                        <p style="color: #666; font-size: 0.75rem; margin: 0;">12.8K vues</p>
                    </div>
                </div>

                <div style="display: flex; gap: 10px; cursor: pointer;" onclick="playVideo('3tmd-ClpJxA')">
                    <div style="width: 60px; height: 45px; background: #4472c4; border-radius: 6px; display: flex; align-items: center; justify-content: center; color: white; font-size: 0.8rem;">
                        <i class="fas fa-play"></i>
                    </div>
                    <div style="flex: 1;">
                        <h5 style="color: #333; font-size: 0.85rem; margin-bottom: 3px; line-height: 1.2;">Nature Africaine</h5>
                        <p style="color: #666; font-size: 0.75rem; margin: 0;">9.5K vues</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Newsletter -->
        <div style="background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 8px 25px rgba(0,0,0,0.1);">
            <h3 style="background: #28a745; color: white; padding: 15px 20px; margin: 0; font-size: 16px; display: flex; align-items: center; gap: 10px;">
                <i class="fas fa-bell"></i>
                Notifications
            </h3>
            <div style="padding: 20px;">
                <p style="color: #666; font-size: 0.9rem; margin-bottom: 15px;">Ne manquez aucune nouvelle émission !</p>
                <input type="email" placeholder="Votre email" style="width: 100%; padding: 10px; border: 2px solid #dee2e6; border-radius: 8px; margin-bottom: 10px; font-size: 0.9rem;">
                <button style="background: #28a745; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-weight: 600; width: 100%;">
                    S'abonner
                </button>
            </div>
        </div>
    </div>
</div>

<style>
.show-card:hover,
.emission-card:hover {
    transform: translateY(-8px);
}

.emission-card:hover .fas.fa-play {
    opacity: 1 !important;
}

.category-filter:hover,
.category-filter.active {
    background: #28a745 !important;
    color: white !important;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(40, 167, 69, 0.3);
}

@media (max-width: 768px) {
    .main-content > div {
        grid-template-columns: 1fr !important;
        gap: 20px !important;
    }
}
</style>

<script>
function playVideo(videoId) {
    window.open(`https://www.youtube.com/watch?v=${videoId}`, '_blank');
}

// Category filtering
document.addEventListener('DOMContentLoaded', function() {
    const categoryFilters = document.querySelectorAll('.category-filter');
    const emissionCards = document.querySelectorAll('.emission-card');
    const showCards = document.querySelectorAll('.show-card');

    categoryFilters.forEach(filter => {
        filter.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Update active filter
            categoryFilters.forEach(f => f.classList.remove('active'));
            this.classList.add('active');
            
            const category = this.dataset.category;
            
            // Filter emission cards
            emissionCards.forEach(card => {
                if (category === 'all' || card.dataset.category === category) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });

            // Filter show cards
            showCards.forEach(card => {
                if (category === 'all' || card.dataset.category === category) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    // Video card click handlers
    const emissionCardsClick = document.querySelectorAll('.emission-card');
    emissionCardsClick.forEach(card => {
        card.addEventListener('click', function() {
            const videoId = this.dataset.videoId;
            if (videoId) {
                window.open(`https://www.youtube.com/watch?v=${videoId}`, '_blank');
            }
        });
    });
});
</script>
{% endblock %}