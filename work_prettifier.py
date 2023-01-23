from leak_detection import Leak
from IPython.display import display, HTML


def create_leak_row(leak: Leak) -> str:
    return f"""
    <tr class="danger">
        <td width="40%">Currently leaking {leak.flow_loss} flow per second; {round(leak.flow_loss_coefficient, 2) * 100}% of junction flow</td>
        <td>Junction {leak.from_node}</td>
        <td>Highest</td>
    </tr>
    """


def create_prediction_row(prediction: tuple[tuple[int, int], float]) -> str:
    if round(prediction[1], 2) == 0:
        return ""

    return f"""
    <tr class="warning">
        <td width="40%">Could potentially leak on temperature change more extreme than {round(prediction[1], 2)} degrees Celcius</td>
        <td>Pipe {prediction[0]}</td>
        <td>Medium</td>
    </tr>
    """


def display_work_todo(leaks: [Leak], predictions) -> None:

    leak_rows = "\n".join([create_leak_row(leak) for leak in leaks])
    prediction_rows = "\n".join([create_prediction_row(prediction) for prediction in predictions[:5]])

    display(HTML(
        f"""
        <!doctype html>
        <html lang="en">
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
            </head>
            <body>
                <table class="table">
                    <thead>
                        <tr>
                            <th scope="col" width="40%">Fault</th>
                            <th scope="col">Location</th>
                            <th scope="col">Priority</th>
                        </tr>
                    </thead>
                    <tbody>
                        {leak_rows}
                        {prediction_rows}
                    </tbody>
                </table>
            </body>
        </html>
        """
    ))
