$(document).bind("scroll", scrolling);

let page = 0;

window.onload = loader();

function scrolling() {
    if ($(window).scrollTop() === $(document).height() - $(window).height()) {
        loader();
    }
}

function loader() {
    $.ajax({
            url: '/api/posts',
            type: 'GET',
        }
    ).done(function (data) {
        let posts = data.posts;
        let leftCol = $('#left');
        let rightCol = $('#right');
        for (let n = page; n <= page + 10; ++n) {
            let card = $(document.querySelector('template#content-block').content).children('.card').clone();
            card.children('img').attr('src', posts[n].photo_url);
            card.children('div').children('a').attr('href', 'https://vk.com/squared_fish?w=wall-112055138_' + posts[n].vk_id);
            if (n % 2 == 0) {
                leftCol.append(card);

            } else {
                rightCol.append(card);
            }
        }
        page += 11;
    })
}