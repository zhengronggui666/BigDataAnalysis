from __future__ import division
import os
import operator
from homework_6 import utils as utils

# 获得ratings的数据
def get_data(file):
    if not os.path.exists(file):
        return {}
    linenum = 0
    data = []
    fp = open(file)
    for line in fp:

        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(",")
        data.append([item[0], item[1], float(item[2]), int(item[3])])

    fp.close()
    return data

# 获取用户标签喜爱度
def get_user_tags(item_cate,data):

    record = {}
    user_tags = {}
    topk = 2  #找到用户电影标签喜爱度前两名

    # userid,itemid,rating,time = item[0],item[1],float(item[2]),int(item[3])
    for item in data:
        userid, itemid, rating, time=item[0],item[1],item[2],item[3]
        # 当用户对电影评分小于4分时,不参与计算标签喜爱度
        if rating < 2:
            continue
        # 将时间戳的映射成0-1的加权数
        time_score = utils.get_time_score(time)
        if userid not in record:
            record[userid] = {}
        for fix_cate in item_cate[itemid]:
            if fix_cate not in record[userid]:
                record[userid][fix_cate] = 0
            record[userid][fix_cate] += rating * time_score * item_cate[itemid][fix_cate]

    # 计算用户标签喜爱度前两名,并将两个比重的和映射为1,便于后续根据比重推荐电影数
    for userid in record:
        if userid not in user_tags:
            user_tags[userid]=[]
        total = 0
        for combo in sorted(record[userid].items(),key=operator.itemgetter(1),reverse=True)[:topk]:
            user_tags[userid].append((combo[0],combo[1]))
            total += combo[1]
        for index in range(len(user_tags[userid])):
            user_tags[userid][index] = (user_tags[userid][index][0],round(user_tags[userid][index][1]/total,3))
    return user_tags

'''
cate_item_sort: 根据标签和评分排序的电影列表
user_tags: 用户标签喜爱度前两名及比重
'''
# 推荐
def recommend(cate_item_sort,user_tags,userid,topk=3):
    
    if userid not in user_tags:
        return {}
    recom_result = {}
    if userid not in recom_result:
        recom_result[userid] = []
    for tag in user_tags[userid]:
        cate = tag[0]
        ratio = tag[1]
        num = round(topk*ratio)
        if cate not in cate_item_sort:
            continue
        recom_list = cate_item_sort[cate][:num]
        recom_result[userid] += recom_list

    return  recom_result


def run_main():
    data = get_data('./ratings.csv')
    avg_score = utils.get_avg("./ratings.csv")
    item_cate, cate_item_sort = utils.get_item_cate("./movies.csv", avg_score)


    user_tags = get_user_tags(item_cate,data)
    # user_tags=utils.user_tags
    return data,user_tags,cate_item_sort
