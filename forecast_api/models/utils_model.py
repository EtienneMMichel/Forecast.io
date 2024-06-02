import json

def register_all_models():
    '''
    automatically list class and their attributes 
    '''
    pass
    

def get_registery():
    registery = dict()
    with open("./registery.json", encoding='utf-8') as fh:
        registery = json.load(fh)

    res = {}
    for model_class, model_blueprint in registery.items() :
        if model_blueprint.is_torch_model:
            pass
            # add all saved models in key : saved models
            # infos are contained inside file saved during the training
            # define model_name
            # define model_config
            # res[model_name] = model_config
        else:
            res[model_class] = model_blueprint
            # replace train_setting by a value

    return res
