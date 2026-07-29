
import time


def run_ai_with_fallback(
    ai_function,
    fallback_function,
    *args,
    **kwargs
):

    try:

        result = ai_function(
            *args,
            **kwargs
        )

        return {
            "success": True,
            "data": result,
            "message": None
        }


    except Exception as e:

        error_message = str(e).lower()


        if (
            "rate limit" in error_message
            or
            "quota" in error_message
            or
            "429" in error_message
            or
            "limit exceeded" in error_message
        ):

            fallback_result = fallback_function(
                *args,
                **kwargs
            )


            return {

                "success": False,

                "data": fallback_result,

                "message":
                "AI quota temporarily exceeded. "
                "Showing local analysis until quota resets."

            }


        raise e