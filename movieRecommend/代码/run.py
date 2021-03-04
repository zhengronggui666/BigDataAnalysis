from homework_6 import content_based as cb
from homework_6 import user_movie as um


if __name__ == '__main__':

    results={}
    # 协同过滤算法的数据准备
    fileData, umdata, similar_list=um.run_main()
    # CB算法的数据准备
    data, user_tags,cate_item_sort=cb.run_main()
    for key in similar_list.keys():
        # print(similar_list[key][1])
        result=um.recommend(fileData,key,similar_list[key][0],similar_list[key][1])
        # result不等于-1时采用CF算法
        if result!=-1:
            results.update(result)
        # result等于-1时使用CB算法
        else:
            result=cb.recommend(cate_item_sort,user_tags,key)

            results.update(result)
    print(results)
    # 将结果写入文件
    fp=open('./movie.csv','w',encoding='utf-8')
    fp.write('userId,movieId\n')
    for key in results.keys():
        for item in results[key]:
            line=key+","+item[0]+"\n"
            fp.write(line)
    fp.close()







