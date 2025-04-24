from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from rag_llm_model.main import main 
import ast

llm_blp = Blueprint("llm", __name__, url_prefix="/llm", description="LLM")

@llm_blp.route("/<symptons>")
class Register(MethodView):
    def get(self, symptons):
        result = main(symptons)["choices"][0]["message"]["content"]

        array = ast.literal_eval(result)
        return jsonify({"synonyms": result}), 200
