$(document).bind("scroll", scrolling);

let page = 0;

window.onload = loader();

function scrolling() {
    if ($(window).scrollTop() == $(document).height() - $(window).height()) {
        loader();
    }
}

function loader() {
    $.ajax({
            url: '/api/posts',
            type: 'GET',
        }
    ).done(function (data) {
        let wrapper = $('.wrapper');
        let posts = data.posts;
        for (let n = page; n <= page + 5; ++n) {
            let content = $(
                document.querySelector('template#content-block').content).children('div').clone();
            content.children('img').attr('src', posts[n].photo_url);
            content.children('a').attr('href', 'https://vk.com/squared_fish?w=wall-112055138_' + posts[n].vk_id);
            wrapper.append(content);
        }
        page += 6;
    })
}