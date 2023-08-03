import time

from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from flask import Flask, render_template
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from werkzeug.exceptions import InternalServerError
from sleep import sleep

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Set global TracerProvider before instrumenting
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "azure-python-server"})
    )
)
tracer = trace.get_tracer(__name__)

# Enable tracing for Flask library
FlaskInstrumentor().instrument_app(app)

# Enable tracing for requests library
RequestsInstrumentor().instrument()

trace_exporter = AzureMonitorTraceExporter(
    connection_string=Config.CONNECTION_STRING
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(trace_exporter)
)


@app.errorhandler(InternalServerError)
def handle_500(e):
    original = getattr(e, "original_exception", None)

    if original is None:
        # direct 500 error, such as abort(500)
        return 500

    # wrapped unhandled error
    return render_template(e=original), 500


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/sleep")
def sleep_route():
    with tracer.start_as_current_span("sleep"):
        print("request received to wake")
        sleep(Config.SLEEP_DURATION, tracer)
    return "i'm awake!"


@app.route("/error")
def error():
    # try:
    raise Exception("error exception")
    # except Exception as err:
    #     print(err)


if __name__ == "__main__":
    print(f"Server is Running on Port: {8080}...")
    app.run(debug=True, port=8080)
