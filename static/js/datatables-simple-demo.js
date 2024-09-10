// window.addEventListener('DOMContentLoaded', event => {
//     // Simple-DataTables
//     // https://github.com/fiduswriter/Simple-DataTables/wiki

//     const datatablesSimple = document.getElementById('datatablesSimple');
//     if (datatablesSimple) {
//         new simpleDatatables.DataTable(datatablesSimple);
//     }
// });



// 상단의 start bootstarp이 제공하는 js코드 주석 처리 후
// Ai에게 도움을 받아 작성한 하단 코드
window.addEventListener('DOMContentLoaded', event => {
    const datatablesSimple = document.getElementById('datatablesSimple');
    if (datatablesSimple) {
        new simpleDatatables.DataTable(datatablesSimple, {
        perPage: 10,
        perPageSelect: [5, 10, 15, 20, 25],
        columns: [
            { select: 0, sort: "asc" },
            { select: 1, sort: "asc" },
            { select: 2, sort: "asc" },
            { select: 3, sort: "asc" },
            { select: 4, sort: "asc" },
            { select: 5, sort: "asc" },
          // 여기에 각 열에 대한 설정을 추가하세요
          // 예: { select: 0, sort: "asc" },
        ],
        labels: {
            placeholder: "검색...",
            perPage: "개씩 보기",
            noRows: "데이터가 없습니다.",
            info: "전체 {rows}개 중 {start}부터 {end}까지 표시",
        },
        });
    }
});