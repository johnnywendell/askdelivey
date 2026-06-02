document.addEventListener('DOMContentLoaded', function () {

    /*
    ============================
    PREVIEW DE FOTO
    ============================
    */
    const inputFoto = document.querySelector('input[type="file"]');
    const preview = document.getElementById('preview');

    if (inputFoto && preview) {

        inputFoto.addEventListener('change', function (e) {

            const file = e.target.files[0];

            if (file) {
                preview.src = URL.createObjectURL(file);
            }

        });

    }


    /*
    ============================
    SIDEBAR MOBILE
    ============================
    */
    const sidebar = document.getElementById('sidebar');
    const toggle = document.getElementById('sidebarToggle');
    const backdrop = document.getElementById('sidebarBackdrop');

    if (toggle && sidebar && backdrop) {

        toggle.addEventListener('click', function () {

            sidebar.classList.toggle('show');
            backdrop.classList.toggle('show');

        });

        backdrop.addEventListener('click', function () {

            sidebar.classList.remove('show');
            backdrop.classList.remove('show');

        });

    }


    /*
    ============================
    TRACKING GLOBAL ENTREGADOR
    ============================
    */

    const trackingBtn =
        document.getElementById('trackingToggleBtn');

    const trackingStatus =
        document.getElementById('trackingStatus');

    const trackingLat =
        document.getElementById('trackingLat');

    const trackingLng =
        document.getElementById('trackingLng');

    if (
        trackingBtn &&
        trackingStatus &&
        trackingLat &&
        trackingLng
    ) {

        let watchId = null;

        let online =
            localStorage.getItem('tracking_online') === 'true';

        atualizarUI();

        /*
        ============================
        BOTÃO
        ============================
        */

        trackingBtn.addEventListener('click', function () {

            if (!online) {
                iniciarTracking();
            } else {
                pararTracking();
            }

        });


        /*
        ============================
        INICIAR TRACKING
        ============================
        */

        function iniciarTracking() {

            if (!navigator.geolocation) {

                trackingStatus.className =
                    'alert alert-danger mb-2';

                trackingStatus.innerText =
                    'Geolocalização não suportada';

                return;
            }

            online = true;

            localStorage.setItem(
                'tracking_online',
                'true'
            );

            atualizarUI();

            watchId =
                navigator.geolocation.watchPosition(
                    enviarLocalizacao,
                    erroGPS,
                    {
                        enableHighAccuracy: true,
                        maximumAge: 0,
                        timeout: 5000
                    }
                );
        }


        /*
        ============================
        PARAR TRACKING
        ============================
        */

        function pararTracking() {

            online = false;

            localStorage.setItem(
                'tracking_online',
                'false'
            );

            if (watchId) {

                navigator.geolocation.clearWatch(
                    watchId
                );

            }

            atualizarUI();
        }


        /*
        ============================
        UI
        ============================
        */

        function atualizarUI() {

            if (online) {

                trackingBtn.innerText =
                    'Ficar OFFLINE';

                trackingBtn.classList.remove(
                    'btn-success'
                );

                trackingBtn.classList.add(
                    'btn-danger'
                );

                trackingStatus.className =
                    'alert alert-success mb-2';

                trackingStatus.innerText =
                    'Online e rastreando';

            } else {

                trackingBtn.innerText =
                    'Ficar ONLINE';

                trackingBtn.classList.remove(
                    'btn-danger'
                );

                trackingBtn.classList.add(
                    'btn-success'
                );

                trackingStatus.className =
                    'alert alert-secondary mb-2';

                trackingStatus.innerText =
                    'Offline';
            }
        }


        /*
        ============================
        ERRO GPS
        ============================
        */

        function erroGPS(error) {

            trackingStatus.className =
                'alert alert-danger mb-2';

            trackingStatus.innerText =
                'Erro GPS: ' + error.message;

            console.error(error);
        }


        /*
        ============================
        ENVIAR LOCALIZAÇÃO
        ============================
        */

        async function enviarLocalizacao(position) {

            const lat =
                position.coords.latitude;

            const lng =
                position.coords.longitude;

            const speed =
                position.coords.speed || 0;

            const heading =
                position.coords.heading || 0;

            trackingLat.innerText = lat;
            trackingLng.innerText = lng;

            try {

                const response =
                    await fetch('/api/tracking/location/', {

                        method: 'POST',

                        credentials: 'same-origin',

                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCSRFToken()
                        },

                        body: JSON.stringify({
                            lat: lat,
                            lng: lng,
                            speed: speed,
                            heading: heading,
                            disponivel: online
                        })

                    });

                if (!response.ok) {

                    trackingStatus.className =
                        'alert alert-danger mb-2';

                    trackingStatus.innerText =
                        'Erro ao enviar localização';

                    return;
                }

                trackingStatus.className =
                    'alert alert-success mb-2';

                trackingStatus.innerText =
                    'Localização enviada';

            } catch (e) {

                console.error(e);

                trackingStatus.className =
                    'alert alert-danger mb-2';

                trackingStatus.innerText =
                    'Erro ao enviar localização';
            }
        }


        /*
        ============================
        CSRF TOKEN
        ============================
        */

        function getCSRFToken() {

            const cookies =
                document.cookie.split(';');

            for (let cookie of cookies) {

                cookie = cookie.trim();

                if (
                    cookie.startsWith('csrftoken=')
                ) {

                    return cookie.substring(
                        'csrftoken='.length
                    );
                }
            }

            return '';
        }


        /*
        ============================
        AUTO RETORNO ONLINE
        ============================
        */

        if (online && !watchId) {
            iniciarTracking();
        }

    }
            /*
        ====================================
        MINIMIZAR TRACKING
        ====================================
        */

        const trackingWidget = document.getElementById('tracking-widget');
        const trackingMinimize = document.getElementById('trackingMinimize');

        if (trackingWidget && trackingMinimize) {

            trackingMinimize.addEventListener('click', function () {

                trackingWidget.classList.toggle('minimized');

                const icon = trackingMinimize.querySelector('i');

                if (trackingWidget.classList.contains('minimized')) {

                    icon.classList.remove('bi-dash-lg');
                    icon.classList.add('bi-geo-alt-fill');

                } else {

                    icon.classList.remove('bi-geo-alt-fill');
                    icon.classList.add('bi-dash-lg');
                }
            });
        }

});