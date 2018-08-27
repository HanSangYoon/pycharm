



def getCScore(returnedResultDictVaules):
    # C_SCORE
    # 거주지, 출신지, 팔로우 수 (returnedResult : 미리 받아온 세부 데이터)이용하여 C_SCORE 산출하기
    c_score_count = 0

    like_cnt_int = 0
    cnt_like_img = 0
    for search_c in returnedResultDictVaules:
        try:
            if '거주' in search_c:
                print('거주지 정보 검색 중...')
                c_score_count_detail = 0
                # print("%%", c_score_count)

                if '서울' in search_c:
                    print('가산 근거 : 거주지가 서울일 경우 10점이 가산 됩니다.')
                    c_score_count_detail += 10
                    c_score_count += c_score_count_detail
                    # print("%%", c_score_count)
                elif '경기' in search_c:
                    print('가산 근거 : 거주지가 경기일 경우 5점이 가산됩니다.')
                    c_score_count_detail += 5
                    c_score_count += c_score_count_detail
                    # print("%%", c_score_count)
                else:
                    print('가산 근거 : 거주지가 비-수도권일 경우 3점이 가산됩니다.')
                    c_score_count_detail += 3
                    c_score_count += c_score_count_detail
                    # print("%%", c_score_count)

            if '출신' in search_c:
                print('출신지 정보 검색 중...')
                c_score_count_detail = 0
                # print("%%", c_score_count)

                if '서울' in search_c:
                    print('가산 근거 : 출신지가 서울일 경우 10점이 가산 됩니다.')
                    c_score_count_detail += 10
                    c_score_count += c_score_count_detail
                    # print("%%", c_score_count)
                elif '경기' in search_c:
                    print('가산 근거 : 출신지가 경기일 경우 5점이 가산됩니다.')
                    c_score_count_detail += 5
                    c_score_count += c_score_count_detail
                    # print("%%", c_score_count)
                else:
                    print('가산 근거 : 출신지가 비-수도권일 경우 3점이 가산됩니다.')
                    c_score_count_detail += 3
                    c_score_count += c_score_count_detail
                    # print("%%", c_score_count)

            if '팔로우' in search_c:

                followCntVal = str(search_c).split('명이')
                followCnt = int(followCntVal[0])
                print('팔로우 수: ', followCnt)
                c_score_count_detail = 0

                if followCnt >= 50:
                    print('팔로워 수가 50명 이상일 경우 10점이 가산됩니다.')
                    c_score_count_detail += 10
                    c_score_count += c_score_count_detail
                    # print("%%", c_score_count)
                elif 40 <= followCnt < 50:
                    print('팔로워 수가 40명 이상 50명 미만일 경우 8점이 가산됩니다.')
                    c_score_count_detail += 8
                    c_score_count += c_score_count_detail
                    # print("%%", c_score_count)
                elif 30 <= followCnt < 40:
                    print('팔로워 수가 30명 이상 40명 미만일 경우 6점이 가산됩니다.')
                    c_score_count_detail += 6
                    c_score_count += c_score_count_detail
                    # print("%%", c_score_count)
                elif 20 <= followCnt < 30:
                    print('팔로워 수가 20명 이상 30명 미만일 경우 4점이 가산됩니다.')
                    c_score_count_detail += 4
                    c_score_count += c_score_count_detail
                    # print("%%", c_score_count)
                elif 10 <= followCnt < 20:
                    print('팔로워 수가 10명 이상 20명 미만일 경우 2점이 가산됩니다.')
                    c_score_count_detail += 2
                    c_score_count += c_score_count_detail
                    # print("%%", c_score_count)
                elif 1 <= followCnt < 10:
                    print('팔로워 수가 1명 이상 10명 미만일 경우 1점이 가산됩니다.')
                    c_score_count_detail += 1
                    c_score_count += c_score_count_detail
                    # print("%%", c_score_count)
                else:
                    print('팔로워가 없으므로 가산점이 부여되지 않습니다. ')
                    c_score_count_detail += 0
                    c_score_count += c_score_count_detail
                    # print("%%", c_score_count)

        except Exception as e_c:
            print('C SCORE EXCEPTION :', e_c)

    # (returnedResult : 미리 받아온 세부 데이터)를 이용하지 않고, 친구 수 값을 추출하여 C_SCORE를 산출하기

    print('C SCORE :', c_score_count)
    print()

    ###############################################################################_C_Score수정중#####################################################
    # friend count
    try:
        autoScrolled_data_soup_html_result = autoScroller(driver)
        userContent_FriendList = autoScrolled_data_soup_html_result.find('div', attrs={
            'id': 'profile_timeline_tiles_unit_pagelets_friends'})

        if userContent_FriendList:
            print('친구 리스트 공개 중입니다.')
            # friendsCnt_str = autoScrolled_data_soup_html_result.select('profile_timeline_tiles_unit_pagelets_friends > li > div > div > div > div:nth-of-type(1) > div > div > div:nth-of-type(2) > div > span')[0].text
            friendsCnt_str = autoScrolled_data_soup_html_result.select(
                '#profile_timeline_tiles_unit_pagelets_friends > li > div > div:nth-of-type(1) > div > div.clearfix._3-8t._2pi4 > div > div > div:nth-of-type(2) > div > span._50f8._2iem > a')[
                0].text

            print(friendsCnt_str)
            friendsCnt = int(friendsCnt_str.split('명')[0].replace(',', ''))

            returnedResultDict['친구수'] = int(friendsCnt_str.split('명')[0].replace(',', ''))

            print('친구 수 : ', friendsCnt)
            if friendsCnt >= 500:
                print('친구 수가 500명 이상일 경우 10점이 가산됩니다.')
                c_score_count_detail += 10
                c_score_count += c_score_count_detail
                # print("%%", c_score_count)
            elif 400 <= friendsCnt < 500:
                print('친구 수가 400명 이상 500명 미만일 경우 8점이 가산됩니다.')
                c_score_count_detail += 8
                c_score_count += c_score_count_detail
                # print("%%", c_score_count)
            elif 300 <= friendsCnt < 400:
                print('친구 수가 300명 이상 400명 미만일 경우 6점이 가산됩니다.')
                c_score_count_detail += 6
                c_score_count += c_score_count_detail
                # print("%%", c_score_count)
            elif 200 <= friendsCnt < 300:
                print('친구 수가 200명 이상 300명 미만일 경우 4점이 가산됩니다.')
                c_score_count_detail += 4
                c_score_count += c_score_count_detail
                # print("%%", c_score_count)
            elif 100 <= friendsCnt < 200:
                print('친구 수가 100명 이상 200명 미만일 경우 2점이 가산됩니다.')
                c_score_count_detail += 2
                c_score_count += c_score_count_detail
                # print("%%", c_score_count)
            elif 1 <= friendsCnt < 100:
                print('친구 수가 1명 이상 100명 미만일 경우 1점이 가산됩니다.')
                c_score_count_detail += 1
                c_score_count += c_score_count_detail
                # print("%%", c_score_count)
            else:
                print('친구가 없으므로 가산점이 부여되지 않습니다. ')
                c_score_count_detail += 0
                c_score_count += c_score_count_detail
                # print("%%", c_score_count)
        else:
            print('친구 리스트가 비공개로 설정되어 있습니다.')

    except Exception as ex:
        print('친구 수 추적에 실패했습니다.', ex)

    likePushPersonCnt = 0

    try:
        attrValue_like_imgVal = autoScrolled_data_soup_html_result.select(
            'ol[data-pnref="story"] > div._5pcb._4b0l > div._4-u2.mbm._4mrt._5jmm._5pat._5v3q._4-u8 > div._3ccb > div._5pcr.userContentWrapper > div:nth-of-type(2) > form.commentable_item > div.uiUfi.UFIContainer._3-a6._4eno._1blz._5pc9._5vsj._5v9k > div.UFIList > div.UFIRow.UFILikeSentence._4204._4_dr > div.clearfix > div > div._1vaq > div._ipp > div._3t53._4ar-._ipn > span._3t54 > a._3emk._401_')
        cnt_like_img = len(attrValue_like_imgVal)

        attrValue_like_txtVal = autoScrolled_data_soup_html_result.select(
            'ol[data-pnref="story"] > div._5pcb._4b0l > div._4-u2.mbm._4mrt._5jmm._5pat._5v3q._4-u8 > div._3ccb > div._5pcr.userContentWrapper > div:nth-of-type(2) > form.commentable_item > div.uiUfi.UFIContainer._3-a6._4eno._1blz._5pc9._5vsj._5v9k > div.UFIList > div.UFIRow.UFILikeSentence._4204._4_dr > div.clearfix > div > div._1vaq > div._ipp > div._3t53._4ar-._ipn > a._2x4v > span._4arz > span')

        likeManCnt = 0
        likeManCnt1 = 0

        for likePerson in range(len(attrValue_like_txtVal)):
            like_cnt_str = attrValue_like_txtVal[likePerson].text.split('명')[0]

            try:
                like_cnt_int = like_cnt_int + int(like_cnt_str)
                # print('"좋아요" 표시 전체 갯수 :', like_cnt_int)
                likePushPersonCnt += 1

            except ValueError as e_p:
                like_man = attrValue_like_txtVal[likePerson].text
                likePushPersonCnt += 1
                # 갯수가 표시되지 않고 사람 이름이 표시된 경우에 해당함.
                # print('"좋아요"를 누른 사람의 이름:', like_man)
                if '외' in like_man:
                    likeManCntStr = like_man.split('외')[1].strip()
                    likeManCnt1 = int(likeManCntStr.split('명')[0])
                else:
                    print('"좋아요"를 누른 사람의 이름:', like_man)
            likeManCnt += likeManCnt1
        print('Total like man count : ', likeManCnt)

        if likeManCnt >= 5000:
            print('좋아요 표시가 5000개 이상일 경우 10점이 가산됩니다.')
            c_score_count_detail += 10
            c_score_count += c_score_count_detail
            # print("%%", m_score_count)
        elif 4000 <= likeManCnt < 5000:
            print('좋아요 표시가 4000개 이상 5000개 미만일 경우 8점이 가산됩니다.')
            c_score_count_detail += 8
            c_score_count += c_score_count_detail
            # print("%%", m_score_count)
        elif 3000 <= likeManCnt < 4000:
            print('좋아요 표시가 3000개 이상 4000개 미만일 경우 6점이 가산됩니다.')
            c_score_count_detail += 6
            c_score_count += c_score_count_detail
            # print("%%", m_score_count)
        elif 2000 <= likeManCnt < 3000:
            print('좋아요 표시가 2000개 이상 3000개 미만일 경우 4점이 가산됩니다.')
            c_score_count_detail += 4
            c_score_count += c_score_count_detail
            # print("%%", m_score_count)
        elif 1000 <= likeManCnt < 2000:
            print('좋아요 표시가 1000개 이상 2000개 미만일 경우 2점이 가산됩니다.')
            c_score_count_detail += 2
            c_score_count += c_score_count_detail
            # print("%%", m_score_count)
        elif 1 <= likeManCnt < 1000:
            print('좋아요 표시가 1개 이상 1000개 미만일 경우 1점이 가산됩니다.')
            c_score_count_detail += 1
            c_score_count += c_score_count_detail
            # print("%%", m_score_count)
        else:
            print('좋아요 표시가 없으므로 가산점이 부여되지 않습니다. ')
            c_score_count_detail += 0
            c_score_count += c_score_count_detail
            # print("%%", m_score_count)

    except Exception as e_lk:
        print('좋아요 정보 추출 Exception', e_lk)

    print('좋아요_사람 전체 명수 : ', likePushPersonCnt)
    print('좋아요(image)__표시 전체 갯수: ', cnt_like_img)

    ###############################################################################_C_Score수정중#####################################################

    returnedResultDict.update({'좋아요__사람전체명수': likePushPersonCnt, '좋아요(image)__표시전체갯수': cnt_like_img})

    return c_score_count

