from bin.utils.utils import manipulated_string
def ResponseData(statusCode, success, error, data):
    return {
        "statusCode": statusCode,
        "success": success,
        "error": error,
        "data": data,
    }

def ResponseDataWithPagination(statusCode, success, error, params, temp):
    items = []
    totalPage = round(temp.total / temp.size)
    nextPage = temp.page + 1
    prevPage = temp.page - 1

    if totalPage == 0:
        totalPage += 1
        nextPage = 0
        prevPage = 0

    if temp.page >= totalPage:
        nextPage = None
        prevPage = totalPage

    if prevPage == temp.page:
        prevPage -= 1


    if len(temp.items) > 0:
        for i in range(len(temp.items)):
            items.append({
                "id":temp.items[i]["invoices_id"],
                "client_id": temp.items[i]["client_id"],
                "sequence_number": temp.items[i]["sequence_number"],
                "recurring": temp.items[i]["recurring"],
                "date": temp.items[i]["date"],
                "due_date": temp.items[i]["due_date"],
                "status_id": temp.items[i]["status_id"],
                "recurring_cycle_id": temp.items[i]["recurring_cycle_id"],
                "sub_total": temp.items[i]["sub_total"],
                "discount_type": temp.items[i]["discount_type"],
                "discount": temp.items[i]["discount"],
                "total": temp.items[i]["total"],
                "received_amount": temp.items[i]["received_amount"],
                "notes": temp.items[i]["notes"],
                "terms": temp.items[i]["terms"],
                "created_by": temp.items[i]["created_by"],
                "deleted_at": temp.items[i]["deleted_at"],
                "created_at": temp.items[i]["created_at"],
                "updated_at": temp.items[i]["updated_at"],
                "status":{
                    "id": temp.items[i]["s_id"],
                    "name": temp.items[i]["status_name"],
                    "class": temp.items[i]["class"],
                    "translated_name": manipulated_string(temp.items[i]["status_name"])
                },
                "client":{
                    "id": temp.items[i]["c_id"],
                    "first_name": temp.items[i]["first_name"],
                    "last_name": temp.items[i]["last_name"],
                    "full_name": f"{temp.items[i]['first_name']} {temp.items[i]['last_name']}"

                },
                "recurring_cycle":{
                    "id": temp.items[i]["rc_id"],
                    "name": temp.items[i]["name"]
                }
            })



    return {
        "statusCode": statusCode,
        "success": success,
        "error": error,
        "totalRecord": temp.total,
        "totalPage":totalPage,
        "prevPage":prevPage,
        "currentPage": temp.page,
        "nextPage":nextPage,
        "data": items,
    }