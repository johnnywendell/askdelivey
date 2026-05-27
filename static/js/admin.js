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

});