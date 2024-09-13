/*!
    * Start Bootstrap - SB Admin v7.0.7 (https://startbootstrap.com/template/sb-admin)
    * Copyright 2013-2023 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE)
    */
    // 
// Scripts
// 

// AI 도움요청
window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});


// AI 도움요청 : localstorage를 사용하여 사용자가 메뉴 로드 후 상태 유지를 위한 작업 요청
document.addEventListener('DOMContentLoaded', function() {
    // 페이지 로드 시 메뉴 상태 복원
    restoreMenuState();

    // 메뉴 클릭 이벤트 리스너 추가
    document.querySelectorAll('.nav-link[data-bs-toggle="collapse"]').forEach(function(element) {
        element.addEventListener('click', function() {
            setTimeout(saveMenuState, 350);
        });
    });
});

function saveMenuState() {
    let menuState = {};
    document.querySelectorAll('.collapse').forEach(function(element) {
        menuState[element.id] = element.classList.contains('show');
    });
    localStorage.setItem('menuState', JSON.stringify(menuState));
}

function restoreMenuState() {
    let menuState = JSON.parse(localStorage.getItem('menuState')) || {};
    for (let id in menuState) {
        let element = document.getElementById(id);
        if (element) {
            if (menuState[id]) {
                new bootstrap.Collapse(element, { toggle: false }).show();
            } else {
                new bootstrap.Collapse(element, { toggle: false }).hide();
            }
        }
    }
}

// 현재 페이지 메뉴 항목 활성화
function setActiveMenuItem() {
    let currentPath = window.location.pathname;
    let menuItem = document.querySelector(`a.nav-link[href$="${currentPath}"]`);
    if (menuItem) {
        menuItem.classList.add('active');
        // 상위 메뉴들도 열기
        let parent = menuItem.closest('.collapse');
        while (parent) {
            new bootstrap.Collapse(parent, { toggle: false }).show();
            parent = parent.parentElement.closest('.collapse');
        }
        saveMenuState();  // 메뉴 상태 저장
    }
}
