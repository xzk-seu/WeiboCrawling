
"""URLs"""

urls_model = {
            # 某地区主页面的URL，决定因素在于地区的编码
            'Home': 'https://weibo.com/p/{code_location}/relateweibo?since_id=&page={page}&display=0&retcode=6102&#39;',
            'JS': ('https://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100101&feed_filter=filter&'
                   'current_page={current_page}&since_id=&page={page}&pagebar={pagebar}&tab=relateweibo&'
                   'pl_name=Pl_Core_MixedFeed__35&id={code_location}&'
                   'script_uri=/p/{code_location}/relateweibo&'
                   'feed_type=1&pre_page={pre_page}&domain_op=100101'),
            'Nearby': ('https://weibo.com/p/1001018008641018500000000/nearby?'
                       'cfs=600&Pl_Core_Pt6Rank__39_filter=&Pl_Core_Pt6Rank__39_page={page}#Pl_Core_Pt6Rank__39'),
        }


