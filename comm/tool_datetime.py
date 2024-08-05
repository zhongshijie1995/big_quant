from comm import tool_classes


@tool_classes.ToolClasses.singleton
class ToolDatetime:
    @staticmethod
    def time_to_minutes(time_str: str):
        hours, minutes = map(int, time_str.split(':'))
        total_minutes = hours * 60 + (minutes % 60)
        return total_minutes

    @staticmethod
    def calc_between_minutes(time_str_1, time_str_2):
        minutes1 = ToolDatetime().time_to_minutes(time_str_1)
        minutes2 = ToolDatetime().time_to_minutes(time_str_2)
        # 假设time_str2是结束时间
        difference = abs(minutes2 - minutes1)
        return difference
