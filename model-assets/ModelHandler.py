from ts.torch_handler.base_handler import BaseHandler
from simpletransformers.question_answering import QuestionAnsweringModel
import torch
import logging
import json

logger = logging.getLogger(__name__)


class ModelHandler(BaseHandler):

    def __init__(self):
        super(ModelHandler, self).__init__()
        self.initialized = False
        self._context = None
        self.model = None
        self.device = None

    def initialize(self, context):

        self._context = context
        self.manifest = context.manifest
        properties = context.system_properties
        model_dir = properties.get("model_dir")

        self.device = torch.device(
            "cuda:" + str(properties.get("gpu_id"))
            if torch.cuda.is_available() and properties.get("gpu_id") is not None
            else "cpu"
        )

        logger.info(f"Device found: {self.device} ...")
        model_dict = {
            'args': {
                "num_train_epochs": 2,
                "max_seq_length": 384,
                "doc_stride": int(384*0.8),
                "train_batch_size": 16,
                "gradient_accumulation_steps": 1,
                "eval_batch_size": 16,
                "save_steps": -1,
                "save_model_every_epoch": True,
                "evaluate_during_training_steps": -1,
                "evaluate_during_training": True,
                "evaluate_during_training_verbose": True,
                "use_cached_eval_features": True
            },
            'type': 'bert'
        }

        self.model = QuestionAnsweringModel(
            model_dict.get('type'),
            model_dir,
            args=model_dict.get('args'),
            use_cuda=str(self.device) != "cpu"
        )

        self.initialized = True

    def preprocess(self, request):
        query = []
        for i, item in enumerate(request):
            data = item.get("data")
            if data is None:
                data = item.get("body")

            try:
                data = json.loads(data.decode('utf-8'))
            except AttributeError:
                pass

            query.append(
                {
                    'context': data.get('context', ''),
                    'qas': [
                        {'id': i, 'question': data.get('question', '')},
                    ]
                }
            )

        return query

    def inference(self, query, *args, **kwargs):
        prediction = self.model.predict(query)

        answers = sorted(prediction[0], key=lambda k: k['id'])
        probs = sorted(prediction[1], key=lambda k: k['id'])

        predicted = [(answers[i], probs[i]) for i in range(len(answers))]

        return predicted

    def postprocess(self, predicted):
        result = []
        for ans, prob in predicted:
            result.append({
                "answers": [
                    {
                        "text": ans['answer'][i],
                        "confidence": prob["probability"][i]
                    } for i in range(len(ans['answer']))
                ],
                "id": ans['id']
            })
        return result

