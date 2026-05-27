/**
 * Template Name: Bootslander - v2.2.0
 * Template URL: https://bootstrapmade.com/bootslander-free-bootstrap-landing-page-template/
 * Author: BootstrapMade.com
 * License: https://bootstrapmade.com/license/
 */


!(function ($) {
    "use strict";

    // Preloader
    $(window).on('load', function () {
        if ($('#preloader').length) {
            $('#preloader').delay(100).fadeOut('slow', function () {
                $(this).remove();
            });
        }
    });

    // Toggle .header-scrolled class
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('#header').addClass('header-scrolled');
        } else {
            $('#header').removeClass('header-scrolled');
        }
    });

    if ($(window).scrollTop() > 100) {
        $('#header').addClass('header-scrolled');
    }

    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });

    $('.back-to-top').click(function () {
        $('html, body').animate({
            scrollTop: 0
        }, 1500, 'easeInOutExpo');
        return false;
    });

    // Venobox
    $(window).on('load', function () {
        $('.venobox').venobox();
    });

    // CounterUp
    $('[data-toggle="counter-up"]').counterUp({
        delay: 10,
        time: 1000
    });

    $(document).ready(function () {
        $('.venobox').venobox();
    });

    // Testimonials carousel
    $(".testimonials-carousel").owlCarousel({
        autoplay: true,
        dots: true,
        loop: true,
        items: 1
    });

    // AOS
    function aos_init() {
        AOS.init({
            duration: 1000,
            easing: "ease-in-out",
            once: true,
            mirror: false
        });
    }

    $(window).on('load', function () {
        aos_init();
    });

})(jQuery);

// Classe active navbar
document.addEventListener("DOMContentLoaded", function () {

    function updateActiveNavbar(hash = null) {

        const currentHash = hash || window.location.hash;

        document.querySelectorAll(".nav-link, .dropdown-item")
            .forEach(link => link.classList.remove("active"));

        document.querySelectorAll(".nav-item.dropdown")
            .forEach(item => item.classList.remove("active"));

        let activeLink = null;

        // Gestion des ancres
        if (currentHash) {

            activeLink = document.querySelector(
                `.dropdown-item[href$="${currentHash}"]`
            );

        } else {

            // Recherche nav-link
            activeLink = document.querySelector(
                `.nav-link[href="${window.location.pathname}"]`
            );

            // Recherche dropdown-item
            if (!activeLink) {
                activeLink = document.querySelector(
                    `.dropdown-item[href="${window.location.pathname}"]`
                );
            }
        }

        if (!activeLink) return;

        activeLink.classList.add("active");

        const parentDropdown = activeLink.closest(".nav-item.dropdown");

        if (parentDropdown) {
            parentDropdown.classList.add("active");
        }
    }

    // Initialisation
    updateActiveNavbar();

    // Changement d'ancre
    window.addEventListener("hashchange", function () {
        updateActiveNavbar(window.location.hash);
    });

    // Clic menu
    document.querySelectorAll(".dropdown-item").forEach(link => {

        link.addEventListener("click", function () {

            const url = new URL(this.href);

            updateActiveNavbar(url.hash);
        });

    });

});

// Mobile Navigation
if ($('.nav-menu').length) {
    const $mobile_nav = $('.nav-menu').clone().prop({
        class: 'mobile-nav d-lg-none'
    });

    $('body').append($mobile_nav);
    $('body').prepend('<button type="button" class="mobile-nav-toggle d-lg-none"><i class="icofont-navigation-menu"></i></button>');
    $('body').append('<div class="mobile-nav-overly"></div>');

    $(document).on('click', '.mobile-nav-toggle', function () {
        $('body').toggleClass('mobile-nav-active');
        $('.mobile-nav-toggle i').toggleClass('icofont-navigation-menu icofont-close');
        $('.mobile-nav-overly').toggle();
    });

    $(document).on('click', '.mobile-nav .nav-item.dropdown > .nav-link, .mobile-nav .drop-down > a', function (e) {
        e.preventDefault();
        $(this).next().slideToggle(300);
        $(this).parent().toggleClass('active');
    });

    $(document).click(function (e) {
        const container = $(".mobile-nav, .mobile-nav-toggle");

        if (!container.is(e.target) && container.has(e.target).length === 0) {
            if ($('body').hasClass('mobile-nav-active')) {
                $('body').removeClass('mobile-nav-active');
                $('.mobile-nav-toggle i').toggleClass('icofont-navigation-menu icofont-close');
                $('.mobile-nav-overly').fadeOut();
            }
        }
    });
}

// ===== SAISIE RECHERCHE ADRESSE =====
window.initAddressAutocomplete = function (scope = document) {
    const input = scope.querySelector('input[name="address"]');
    const suggestionsList = scope.querySelector("#address-suggestions");

    if (!input || !suggestionsList) {
        console.log("Adresse introuvable", {input, suggestionsList});
        return;
    }

    if (input.dataset.autocompleteInitialized === "true") return;
    input.dataset.autocompleteInitialized = "true";

    function closeSuggestions() {
        suggestionsList.innerHTML = "";
    }

    input.addEventListener("input", function () {
        const query = input.value.trim();
        closeSuggestions();

        if (query.length < 3) return;

        fetch(`https://api-adresse.data.gouv.fr/search/?q=${encodeURIComponent(query)}&limit=5`)
            .then(res => res.json())
            .then(data => {
                if (!data.features.length) {
                    suggestionsList.innerHTML = `<li class="list-group-item">Aucune adresse</li>`;
                    return;
                }

                data.features.forEach(feature => {
                    const li = document.createElement("li");
                    li.textContent = feature.properties.label;
                    li.className = "list-group-item list-group-item-action";
                    li.style.cursor = "pointer";

                    li.addEventListener("click", function () {
                        input.value = feature.properties.label;
                        closeSuggestions();
                    });

                    suggestionsList.appendChild(li);
                });
            });
    });
};

document.addEventListener("shown.bs.modal", function (event) {
    if (event.target.id === "adherentModal") {
        initAddressAutocomplete();
    }
});
