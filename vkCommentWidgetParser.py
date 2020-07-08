def get_site_comments(data, source):
    count = 200
    offset = 0
    site_pages = {}
    try:
        while True:
            pages = vk_methods.widgets_get_pages(5104638, offset=offset, count=count)['pages']
            if not pages:
                break
            else:
                for page in pages:
                    site_pages.update({page.get('id', ''): {"id": page.get('id', ''), "url": page.get('url', ''),
                                       "page_id": page.get('page_id', ''), "comments": {"count": 0},
                                       "comments_count": page.get('comments', {}).get('count', 0)}})
            offset += count
        main.send_message(admin_id, 'Pages got, collecting comments', source=source)
        for page_id, page in site_pages.items():
            if page.get('comments_count', 0) > 0:
                count = 200
                offset = 0
                while True:
                    comments = vk_methods.widgets_get_comments(5104638, '', page['page_id'], fields='replies',
                                                               offset=offset, count=count)['posts']
                    if not comments:
                        break
                    else:
                        for comment in comments:
                            page['comments']['count'] += 1
                            page['comments'].update({comment.get('id', ''): {
                                "id": comment.get('id', ''),
                                "user": vk_methods.user_name(comment.get('from_id', '')),
                                "to_id": comment.get('to_id', ''),
                                "date": comment.get('date', ''),
                                "text": comment.get('text', ''),
                                "replies": comment.get('comments', {}).get('replies', []),
                                "likes": comment.get('likes', {}).get('count', []),
                                "reposts": comment.get('reposts', {}).get('count', [])
                            }
                            })
                    offset += count
    except Exception:
        utilities.error_notificator(traceback.format_exc())                    
