def load_palettes():
    from requests import get
    from app import get_db_session
    from app.models import Palette

    LOSPEC_URL = 'https://lospec.com/palette-list/load?'
    is_empty = lambda res: False if res else True

    session = get_db_session()
    all_palettes_slugs = list(map(lambda slug: slug[0], session.query(Palette.slug).all()))
    titles, number = [], 1
    res = get(f'{LOSPEC_URL}colorNumberFilterType=any&colorNumber=8&page=0&tag=&sortingType=newest').json()
    while not is_empty(res['palettes']):
        for palette in res['palettes']:
            if palette['slug'] not in all_palettes_slugs:
                new_pal = Palette(
                    title=palette['title'],
                    slug=palette['slug'],
                    colors=palette['colors']
                )
                session.add(new_pal)
            else:
                session.commit()
                print('Palette was successfully added into a database')
                return
        res = get(f'{LOSPEC_URL}colorNumberFilterType=any&colorNumber=8&page={number}&tag=&sortingType=newest').json()
        number += 1
    session.commit()
    print('Palettes were successfully added into a database')


if __name__ == '__main__':
    loading()
