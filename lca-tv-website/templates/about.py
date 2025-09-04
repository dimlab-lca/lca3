{% extends "base.html" %}

{% block title %}À Propos - LCA TV{% endblock %}

{% block content %}
<div style="display: grid; grid-template-columns: 1fr 350px; gap: 30px; margin-top: 0;">
    <div class="content-left">
        <h1 style="font-size: 32px; color: #28a745; margin-bottom: 10px; text-align: center;">À Propos de LCA TV</h1>
        <p style="color: #666; margin-bottom: 40px; text-align: center; font-size: 16px;">La Chaîne Africaine de Télévision - Votre référence au Burkina Faso</p>
        
        <!-- Hero Section -->
        <div style="background: linear-gradient(135deg, #28a745, #20693e); color: white; border-radius: 20px; padding: 40px; margin-bottom: 40px; text-align: center; position: relative; overflow: hidden;">
            <div style="position: absolute; top: -50px; right: -50px; width: 150px; height: 150px; background: rgba(255,255,255,0.1); border-radius: 50%; opacity: 0.5;"></div>
            <div style="position: absolute; bottom: -30px; left: -30px; width: 100px; height: 100px; background: rgba(255,255,255,0.1); border-radius: 50%; opacity: 0.3;"></div>
            <div style="position: relative; z-index: 2;">
                <div style="width: 100px; height: 100px; background: rgba(255,255,255,0.2); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px; font-size: 2.5rem;">
                    <i class="fas fa-broadcast-tower"></i>
                </div>
                <h2 style="font-size: 2.2rem; margin-bottom: 15px; font-weight: bold;">LCA TV</h2>
                <p style="font-size: 1.1rem; opacity: 0.9; line-height: 1.6;">Depuis plus de 15 ans, nous informons, divertissons et éduquons le peuple burkinabè avec des contenus de qualité qui reflètent notre identité africaine.</p>
            </div>
        </div>

        <!-- Notre Mission -->
        <div style="margin-bottom: 50px;">
            <h2 style="font-size: 1.8rem; color: #333; margin-bottom: 30px; font-weight: bold; display: flex; align-items: center; gap: 10px;">
                <i class="fas fa-bullseye" style="color: #e74c3c;"></i>
                Notre Mission
            </h2>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 25px;">
                <div style="background: white; border-radius: 15px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); text-align: center; border-top: 4px solid #28a745;">
                    <div style="width: 70px; height: 70px; background: linear-gradient(135deg, #28a745, #20693e); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px; color: white; font-size: 1.8rem;">
                        <i class="fas fa-newspaper"></i>
                    </div>
                    <h3 style="color: #333; margin-bottom: 15px; font-size: 1.2rem;">Informer</h3>
                    <p style="color: #666; line-height: 1.6;">Fournir une information fiable, objective et de qualité sur l'actualité nationale et internationale.</p>
                </div>

                <div style="background: white; border-radius: 15px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); text-align: center; border-top: 4px solid #4472c4;">
                    <div style="width: 70px; height: 70px; background: linear-gradient(135deg, #4472c4, #3451a3); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px; color: white; font-size: 1.8rem;">
                        <i class="fas fa-heart"></i>
                    </div>
                    <h3 style="color: #333; margin-bottom: 15px; font-size: 1.2rem;">Divertir</h3>
                    <p style="color: #666; line-height: 1.6;">Proposer des programmes variés qui célèbrent la culture burkinabè et africaine.</p>
                </div>

                <div style="background: white; border-radius: 15px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); text-align: center; border-top: 4px solid #e74c3c;">
                    <div style="width: 70px; height: 70px; background: linear-gradient(135deg, #e74c3c, #c0392b); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px; color: white; font-size: 1.8rem;">
                        <i class="fas fa-graduation-cap"></i>
                    </div>
                    <h3 style="color: #333; margin-bottom: 15px; font-size: 1.2rem;">Éduquer</h3>
                    <p style="color: #666; line-height: 1.6;">Contribuer à l'éducation et à la sensibilisation sur les enjeux de développement.</p>
                </div>
            </div>
        </div>

        <!-- Publicité Banner -->
        <div style="background: linear-gradient(135deg, #f8f9fa, #e9ecef); border-radius: 15px; padding: 30px; margin-bottom: 40px; text-align: center; border: 2px dashed #dee2e6;">
            <h3 style="color: #666; margin-bottom: 15px; font-size: 1.1rem;">PARTENARIAT PUBLICITAIRE</h3>
            <div style="height: 120px; background: white; border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                <div style="text-align: center; color: #adb5bd;">
                    <i class="fas fa-handshake" style="font-size: 2rem; margin-bottom: 10px;"></i>
                    <div style="font-size: 1rem; font-weight: 600;">Devenez notre partenaire</div>
                    <div style="font-size: 0.8rem;">Contactez notre équipe commerciale</div>
                </div>
            </div>
        </div>

        <!-- Nos Valeurs -->
        <div style="margin-bottom: 50px;">
            <h2 style="font-size: 1.8rem; color: #333; margin-bottom: 30px; font-weight: bold; display: flex; align-items: center; gap: 10px;">
                <i class="fas fa-gem" style="color: #f39c12;"></i>
                Nos Valeurs
            </h2>
            
            <div style="background: white; border-radius: 15px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px;">
                    <div style="text-align: center;">
                        <div style="width: 60px; height: 60px; background: #28a745; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; color: white; font-size: 1.5rem;">
                            <i class="fas fa-shield-alt"></i>
                        </div>
                        <h4 style="color: #333; margin-bottom: 10px;">Intégrité</h4>
                        <p style="color: #666; font-size: 0.9rem; line-height: 1.5;">Nous privilégions l'honnêteté et la transparence dans tout ce que nous faisons.</p>
                    </div>

                    <div style="text-align: center;">
                        <div style="width: 60px; height: 60px; background: #4472c4; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; color: white; font-size: 1.5rem;">
                            <i class="fas fa-users"></i>
                        </div>
                        <h4 style="color: #333; margin-bottom: 10px;">Proximité</h4>
                        <p style="color: #666; font-size: 0.9rem; line-height: 1.5;">Nous restons proches de nos téléspectateurs et de leurs préoccupations.</p>
                    </div>

                    <div style="text-align: center;">
                        <div style="width: 60px; height: 60px; background: #e74c3c; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; color: white; font-size: 1.5rem;">
                            <i class="fas fa-star"></i>
                        </div>
                        <h4 style="color: #333; margin-bottom: 10px;">Excellence</h4>
                        <p style="color: #666; font-size: 0.9rem; line-height: 1.5;">Nous visons l'excellence dans la qualité de nos programmes et services.</p>
                    </div>

                    <div style="text-align: center;">
                        <div style="width: 60px; height: 60px; background: #f39c12; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; color: white; font-size: 1.5rem;">
                            <i class="fas fa-globe-africa"></i>
                        </div>
                        <h4 style="color: #333; margin-bottom: 10px;">Africanité</h4>
                        <p style="color: #666; font-size: 0.9rem; line-height: 1.5;">Nous célébrons et promouvons les valeurs et la culture africaines.</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Notre Histoire -->
        <div style="margin-bottom: 50px;">
            <h2 style="font-size: 1.8rem; color: #333; margin-bottom: 30px; font-weight: bold; display: flex; align-items: center; gap: 10px;">
                <i class="fas fa-history" style="color: #4472c4;"></i>
                Notre Histoire
            </h2>
            
            <div style="background: white; border-radius: 15px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
                <div style="border-left: 4px solid #28a745; padding-left: 25px; margin-bottom: 25px;">
                    <h4 style="color: #28a745; margin-bottom: 10px; font-size: 1.1rem;">2008 - Les Débuts</h4>
                    <p style="color: #666; line-height: 1.6;">Création de LCA TV avec pour ambition de devenir la chaîne de référence du Burkina Faso. Nos premiers programmes incluaient le journal télévisé et des émissions culturelles.</p>
                </div>

                <div style="border-left: 4px solid #4472c4; padding-left: 25px; margin-bottom: 25px;">
                    <h4 style="color: #4472c4; margin-bottom: 10px; font-size: 1.1rem;">2015 - Expansion</h4>
                    <p style="color: #666; line-height: 1.6;">Lancement de nouvelles émissions phares comme "Franc Parler" et "7 Afrique". Extension de notre couverture à l'ensemble du territoire national.</p>
                </div>

                <div style="border-left: 4px solid #e74c3c; padding-left: 25px; margin-bottom: 25px;">
                    <h4 style="color: #e74c3c; margin-bottom: 10px; font-size: 1.1rem;">2020 - Numérique</h4>
                    <p style="color: #666; line-height: 1.6;">Transition vers le numérique et lancement de nos plateformes en ligne. Développement de notre présence sur les réseaux sociaux et YouTube.</p>
                </div>

                <div style="border-left: 4px solid #f39c12; padding-left: 25px;">
                    <h4 style="color: #f39c12; margin-bottom: 10px; font-size: 1.1rem;">2024 - Innovation</h4>
                    <p style="color: #666; line-height: 1.6;">Lancement de nouveaux formats interactifs et renforcement de notre engagement envers un journalisme de qualité au service de la démocratie burkinabè.</p>
                </div>
            </div>
        </div>

        <!-- Équipe -->
        <div style="margin-bottom: 40px;">
            <h2 style="font-size: 1.8rem; color: #333; margin-bottom: 30px; font-weight: bold; display: flex; align-items: center; gap: 10px;">
                <i class="fas fa-users-cog" style="color: #28a745;"></i>
                Notre Équipe
            </h2>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 25px;">
                <div style="background: white; border-radius: 15px; padding: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); text-align: center;">
                    <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #28a745, #20693e); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px; color: white; font-size: 2rem;">
                        <i class="fas fa-microphone"></i>
                    </div>
                    <h4 style="color: #333; margin-bottom: 10px;">Journalistes</h4>
                    <p style="color: #666; font-size: 0.9rem; line-height: 1.5;">Une équipe de journalistes expérimentés dédiés à l'information de qualité.</p>
                    <div style="color: #28a745; font-weight: bold; margin-top: 10px;">25+ Professionnels</div>
                </div>

                <div style="background: white; border-radius: 15px; padding: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); text-align: center;">
                    <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #4472c4, #3451a3); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px; color: white; font-size: 2rem;">
                        <i class="fas fa-video"></i>
                    </div>
                    <h4 style="color: #333; margin-bottom: 10px;">Production</h4>
                    <p style="color: #666; font-size: 0.9rem; line-height: 1.5;">Techniciens et producteurs passionnés pour des programmes de qualité.</p>
                    <div style="color: #4472c4; font-weight: bold; margin-top: 10px;">15+ Experts</div>
                </div>

                <div style="background: white; border-radius: 15px; padding: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); text-align: center;">
                    <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #e74c3c, #c0392b); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px; color: white; font-size: 2rem;">
                        <i class="fas fa-cogs"></i>
                    </div>
                    <h4 style="color: #333; margin-bottom: 10px;">Technique</h4>
                    <p style="color: #666; font-size: 0.9rem; line-height: 1.5;">Ingénieurs et techniciens garantissant la qualité de diffusion.</p>
                    <div style="color: #e74c3c; font-weight: bold; margin-top: 10px;">12+ Spécialistes</div>
                </div>
            </div>
        </div>
    </div>

    <div class="sidebar">
        <!-- En Direct -->
        <div style="background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 8px 25px rgba(0,0,0,0.1); margin-bottom: 25px;">
            <h3 style="background: #e74c3c; color: white; padding: 15px 20px; margin: 0; font-size: 16px; display: flex; align-items: center; gap: 10px;">
                <i class="fas fa-broadcast-tower"></i>
                En Direct
            </h3>
            <div style="padding: 20px; text-align: center;">
                <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #e74c3c, #c0392b); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; color: white; font-size: 1.5rem;">
                    <i class="fas fa-tv"></i>
                </div>
                <h4 style="color: #333; margin-bottom: 10px;">Journal du Soir</h4>
                <p style="color: #666; font-size: 0.9rem; margin-bottom: 15px;">Toute l'actualité du jour</p>
                <div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin-bottom: 15px;">
                    <span style="width: 8px; height: 8px; background: #e74c3c; border-radius: 50%; animation: pulse 2s infinite;"></span>
                    <span style="color: #e74c3c; font-weight: bold; font-size: 0.9rem;">EN DIRECT</span>
                </div>
                <button onclick="window.open('{{ url_for('live') }}', '_blank')" style="background: #e74c3c; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-weight: 600; width: 100%;">
                    <i class="fas fa-play"></i> Regarder
                </button>
            </div>
        </div>

        <!-- Statistiques -->
        <div style="background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 8px 25px rgba(0,0,0,0.1); margin-bottom: 25px;">
            <h3 style="background: #28a745; color: white; padding: 15px 20px; margin: 0; font-size: 16px; display: flex; align-items: center; gap: 10px;">
                <i class="fas fa-chart-line"></i>
                En Chiffres
            </h3>
            <div style="padding: 20px;">
                <div style="text-align: center; margin-bottom: 20px;">
                    <div style="font-size: 2rem; font-weight: bold; color: #28a745;">15+</div>
                    <div style="color: #666; font-size: 0.9rem;">Années d'expérience</div>
                </div>
                <div style="text-align: center; margin-bottom: 20px;">
                    <div style="font-size: 2rem; font-weight: bold; color: #4472c4;">2M+</div>
                    <div style="color: #666; font-size: 0.9rem;">Téléspectateurs</div>
                </div>
                <div style="text-align: center; margin-bottom: 20px;">
                    <div style="font-size: 2rem; font-weight: bold; color: #e74c3c;">24/7</div>
                    <div style="color: #666; font-size: 0.9rem;">Heures de diffusion</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2rem; font-weight: bold; color: #f39c12;">50+</div>
                    <div style="color: #666; font-size: 0.9rem;">Émissions régulières</div>
                </div>
            </div>
        </div>

        <!-- Publicité -->
        <div style="background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 8px 25px rgba(0,0,0,0.1); margin-bottom: 25px;">
            <div style="background: #4472c4; color: white; padding: 10px 15px; text-align: center; font-size: 12px; font-weight: bold;">
                PUBLICITÉ
            </div>
            <div style="height: 250px; background: linear-gradient(135deg, #f8f9fa, #e9ecef); display: flex; align-items: center; justify-content: center;">
                <div style="text-align: center; color: #6c757d;">
                    <i class="fas fa-ad" style="font-size: 2rem; margin-bottom: 10px;"></i>
                    <div style="font-weight: 600;">Votre Pub Ici</div>
                    <div style="font-size: 0.8rem;">300 x 250</div>
                </div>
            </div>
        </div>

        <!-- Récompenses -->
        <div style="background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 8px 25px rgba(0,0,0,0.1);">
            <h3 style="background: #f39c12; color: white; padding: 15px 20px; margin: 0; font-size: 16px; display: flex; align-items: center; gap: 10px;">
                <i class="fas fa-trophy"></i>
                Reconnaissances
            </h3>
            <div style="padding: 20px;">
                <div style="margin-bottom: 15px; display: flex; align-items: center; gap: 10px;">
                    <div style="width: 40px; height: 40px; background: #f39c12; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 1rem;">
                        <i class="fas fa-award"></i>
                    </div>
                    <div>
                        <h5 style="color: #333; font-size: 0.9rem; margin-bottom: 2px;">Meilleure Chaîne 2023</h5>
                        <p style="color: #666; font-size: 0.8rem; margin: 0;">Prix du CSC</p>
                    </div>
                </div>

                <div style="margin-bottom: 15px; display: flex; align-items: center; gap: 10px;">
                    <div style="width: 40px; height: 40px; background: #28a745; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 1rem;">
                        <i class="fas fa-medal"></i>
                    </div>
                    <div>
                        <h5 style="color: #333; font-size: 0.9rem; margin-bottom: 2px;">Excellence Journalistique</h5>
                        <p style="color: #666; font-size: 0.8rem; margin: 0;">AJBF 2022</p>
                    </div>
                </div>

                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="width: 40px; height: 40px; background: #4472c4; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 1rem;">
                        <i class="fas fa-star"></i>
                    </div>
                    <div>
                        <h5 style="color: #333; font-size: 0.9rem; margin-bottom: 2px;">Innovation Média</h5>
                        <p style="color: #666; font-size: 0.8rem; margin: 0;">CEDEAO 2021</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

@media (max-width: 768px) {
    .main-content > div {
        grid-template-columns: 1fr !important;
        gap: 20px !important;
    }
}
</style>
{% endblock %}{% extends "base.html" %}

{% block title %}À Propos - LCA TV{% endblock %}

{% block content %}
<section>
    <h1 style="text-align: center; margin-bottom: 2rem; color: #2d8f5f; font-size: 2.5rem;">
        <i class="fas fa-info-circle"></i> À Propos de LCA TV
    </h1>

    <div style="max-width: 800px; margin: 0 auto;">
        <div style="background: white; border-radius: 15px; padding: 3rem; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-bottom: 2rem;">
            <h2 style="color: #2d8f5f; margin-bottom: 1rem;">Notre Mission</h2>
            <p style="margin-bottom: 2rem; line-height: 1.8;">
                LCA TV (La Chaîne Africaine de Télévision) est la chaîne de télévision de référence du Burkina Faso. 
                Nous nous engageons à informer, divertir et éduquer nos téléspectateurs avec des contenus de qualité 
                qui reflètent la richesse culturelle et la diversité de notre pays.
            </p>

            <h2 style="color: #2d8f5f; margin-bottom: 1rem;">Nos Programmes</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-bottom: 2rem;">
                <div style="padding: 1rem; border: 2px solid #2d8f5f; border-radius: 10px;">
                    <h3 style="color: #2d8f5f;"><i class="fas fa-newspaper"></i> Actualités</h3>
                    <p>Journal télévisé, flash info, reportages</p>
                </div>
                <div style="padding: 1rem; border: 2px solid #1e6091; border-radius: 10px;">
                    <h3 style="color: #1e6091;"><i class="fas fa-comments"></i> Débats</h3>
                    <p>Franc-Parler, discussions, analyses politiques</p>
                </div>
                <div style="padding: 1rem; border: 2px solid #2d8f5f; border-radius: 10px;">
                    <h3 style="color: #2d8f5f;"><i class="fas fa-mask"></i> Culture</h3>
                    <p>Patrimoine, traditions, festivals, art</p>
                </div>
                <div style="padding: 1rem; border: 2px solid #1e6091; border-radius: 10px;">
                    <h3 style="color: #1e6091;"><i class="fas fa-futbol"></i> Sport</h3>
                    <p>Étalons du Burkina, compétitions locales</p>
                </div>
            </div>

            <h2 style="color: #2d8f5f; margin-bottom: 1rem;">Notre Équipe</h2>
            <p style="line-height: 1.8;">
                Une équipe de journalistes, techniciens et producteurs passionnés travaille quotidiennement 
                pour vous offrir une programmation de qualité. Nous croyons en l'importance de l'information 
                libre et responsable pour le développement de notre société.
            </p>
        </div>
    </div>
</section>
{% endblock %}