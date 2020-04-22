$(document).bind("scroll", scrolling);

let page = 0;
let groupId = $('#groupId').text();

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
        case '/sug_posts':
            postsType = 'sug';
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
            card.children('div').children('a').attr('href', `https://vk.com/wall${groupId}_${posts[n].vk_id}`);
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
                case 'sug':
                    card.children('div').children('button').addClass('sug');
                    card.children('div').children('button').attr('id', posts[n].vk_id);
                    card.children('div').children('button').html('Редактировать');
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
    });
    targetElem.text('В избранном')
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
    targetElem.parents('.card').remove()
});


$(document).on('click', '.sug', function (event) {
    let targetElem = $(event.target);
    if (targetElem.attr('class') === undefined) {
        targetElem = targetElem.parent('.sug')
    }
    let postId = targetElem.attr('id');
    window.location.href = `/post#${postId}`
});