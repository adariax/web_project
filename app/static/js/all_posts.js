$(document).bind("scroll", scrolling);

let page = 0;

window.onload = loader();

function scrolling() {
    if ($(window).scrollTop() === $(document).height() - $(window).height()) {
        loader();
    }
}

function loader() {
    let postsType = '';
    switch (window.location.pathname) {
        case '/':
            postsType = 'all';
            break;
        case '/fav_posts':
            postsType = 'fav';
            break;
    }
    $.ajax({
            url: `/api/posts?type=${postsType}`,
            type: 'GET',
        }
    ).done(function (data) {
        let posts = data.posts;
        if (page >= posts.length + 11) {
            return
        }
        let leftCol = $('#left');
        let rightCol = $('#right');
        for (let n = page; n <= page + 10; ++n) {
            if (n >= posts.length) {
                break
            }
            let card = $(document.querySelector('template#content-block').content).children('.card').clone();
            card.children('img').attr('src', posts[n].photo_url);
            card.children('div').children('a').attr('href', 'https://vk.com/squared_fish?w=wall-112055138_' + posts[n].vk_id);
            switch (postsType) {
                case 'all':
                    card.children('div').children('button').addClass('fav');
                    card.children('div').children('button').attr('id', (posts[n].id).toString());
                    break;
                case 'fav':
                    card.children('div').children('button').addClass('unfav');
                    card.children('div').children('button').attr('id', (posts[n].id).toString());
                    card.children('div').children('button').html('Удалить из избранного');
                    break;
            }
            if (n % 2 === 0) {
                leftCol.append(card);

            } else {
                rightCol.append(card);
            }
        }
        page = page + 11;
    })
}

$(document).on('click', '.fav', function (event) {
    let targetElem = $(event.target);
    if (targetElem.attr('class') === undefined) {
        targetElem = targetElem.parent('.fav')
    }
    let postId = targetElem.attr('id');
    $.ajax({
        url: `/api/favpost`,
        type: 'POST',
        data: {'post_id': Number(postId)}
    })
});


$(document).on('click', '.unfav', function (event) {
    let targetElem = $(event.target);
    if (targetElem.attr('class') === undefined) {
        targetElem = targetElem.parent('.unfav')
    }
    let postId = targetElem.attr('id');
    $.ajax({
        url: `/api/favpost`,
        type: 'DELETE',
        data: {'post_id': Number(postId)}
    });
    targetElem.addClass('b-disable');
});
