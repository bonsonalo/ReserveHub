from datetime import timedelta




def date_range(start, end):
    current= start

    while current <= end:
        yield current
        current+= timedelta(days= 1) 


def has_conflict(updated, existing_availabilities, existing_booking):
    def check_blocks(blocks):
        for block in blocks:
            for d1 in date_range(updated.start_date, updated.end_date):
                for d2 in date_range(block.start_date, block.end_date):
                    if d1 != d2:
                        continue
                    if updated.start_time < block.end_time and block.start_time < updated.end_time:
                        return True
        return False
    
    return (
        check_blocks(existing_availabilities) or 
        check_blocks(existing_booking)
    )