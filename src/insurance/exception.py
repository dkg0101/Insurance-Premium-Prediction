import os
import sys

def get_detailed_error_message(error_message:Exception,error_detail:sys) -> str:
    """
    This function returns detailed error message for given exception
    """
    _,_,exec_tb = error_detail.exc_info()
    try_block_line_no = exec_tb.tb_lineno
    exception_block_line_no = exec_tb.tb_frame.f_lineno
    file_name = exec_tb.tb_frame.f_code.co_filename
    detailed_error_message = f"""
                    Error occured in script: [{file_name}] 
                    at try block line number: {try_block_line_no} and exception block line number: {exception_block_line_no}
                    Message: [{error_message}]
                    """
    return detailed_error_message

class CustomException(Exception):
    def __init__(self,error_message:Exception,error_detail:sys) :
        super().__init__(error_message)
        self.error_message = get_detailed_error_message(error_message=error_message,error_detail=error_detail)


    def __str__(self):
        return self.error_message

    def __repr__(self) -> str:
        return CustomException.__name__.str()

            

