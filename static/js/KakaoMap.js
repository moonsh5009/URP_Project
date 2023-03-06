function createRange(latlng, radius, color) {
    return new kakao.maps.Circle({
        center : latlng,
        radius: radius * 1000,
        strokeWeight: 5,
        strokeColor: color,
        strokeOpacity: 1,
        strokeStyle: 'dashed',
        fillColor: color,
        fillOpacity: 0.3
    });
}
function createCircle(latlng, color, radius=0.4) {
    return new kakao.maps.Circle({
        center : latlng,
        radius: radius * 1000,
        strokeWeight: 5,
        strokeOpacity: 0.8,
        strokeStyle: 0,
        strokeColor: color,
        fillColor: color,
        fillOpacity: 0.6
    });
}
function createLine(latlng0, latlng1, color, weight=3, alpha=0.7) {
    return new kakao.maps.Polyline({
        path: [latlng0, latlng1],
        strokeWeight: weight,
        strokeColor: color,
        strokeOpacity: alpha,
    });
}
function createPolygon(paths, color) {
    new kakao.maps.Polygon({
        path:paths,
        strokeWeight: 1,
        strokeColor: color,
        strokeOpacity: 1,
        strokeStyle: 0
    }).setMap(map);
}
function createRectangle(latlng0, latlng1, color) {
    var rectBounds = new kakao.maps.LatLngBounds(latlng0, latlng1);
    return new kakao.maps.Rectangle({
        bounds: rectBounds,
        strokeWeight: 3,
        strokeColor: color,
        strokeOpacity: 0.5,
        strokeStyle: 0
    }).setMap(map);
}
function createMarker(latlng, color) {
    return new kakao.maps.Marker({
        position: latlng
    });
}
function createKakaoMap(lat, lng, lev, str) {
    var mapContainer = document.getElementById(str),
    mapOption = { center: new kakao.maps.LatLng(lat, lng), level: lev };
    return new kakao.maps.Map(mapContainer, mapOption);
}
function createLatlng(lat, lng) {
    return new kakao.maps.LatLng(lat, lng);
}

function invisibleHospital() {
    const div = document.getElementById('menu_wrap');
    //if (div.style.display == 'block')
    div.style.display = 'none';
}
function visibleHospital() {
    const div = document.getElementById('menu_wrap');
    if (div.style.display == 'none')
        div.style.display = 'block';
}

function displayHospital(graph, hospitalName){
    var listEl = document.getElementById('placesList'),
    menuEl = document.getElementById('menu_wrap'),
    fragment = document.createDocumentFragment(),
    listStr = '';
    // 검색 결과 목록에 추가된 항목들을 제거합니다]
    while (listEl.hasChildNodes())
        listEl.removeChild (listEl.lastChild);
//
//    // 지도에 표시되고 있는 마커를 제거합니다
//    removeMarker();

    for ( var i=0; i<graph.length; i++ ) {
        itemEl = getListItem(i, graph[i], hospitalName); // 검색 결과 항목 Element를 생성합니다
        fragment.appendChild(itemEl);
    }
    // 검색결과 항목들을 검색결과 목록 Elemnet에 추가합니다
    listEl.appendChild(fragment);

    menuEl.scrollTop = 0;

    // 검색된 장소 위치를 기준으로 지도 범위를 재설정합니다
}

function getListItem(index, places, hospitalName) {

    var el = document.createElement('li'),
    // 병원 이름
    itemStr ='<div class="info">' +'   <h5>' + hospitalName[places.index] + '</h5>';
    //이동중인 환자 agents
    itemStr+='    <span>' +"Scale : " + places.scale + ", Agents : " + places.num + ", Cost : "+ places.cost, + '</span>';
    itemStr+= '    <span>' +"start : " + places.startTime + ", end : "+ places.endTime + '</span>'+
                "</div>";
    el.innerHTML = itemStr;
    el.className = 'item';
    return el;
}