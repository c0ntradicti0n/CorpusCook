# CorpusCook

This repo contains different tools to extract corpora from various sources by customizing the tool in the way I need it.

For instance there is a tool for extracting text from tables, doing OCR on the single cells.

Another thing is a server, that holds the model and corpus manipulation tools on a server for making predictions and updating the corpus in its lifecycle. This means, that corpora get outdated if counterexamples are found, Their corrected annotation should be corrected and added to the corpus.and the model trained again.

Starting the server with 
```
python human_in_loop_SandC/server.py
```

will get it in a state waiting for communication with the corresponding App in [CorpusCookApp](https://github.com/c0ntradicti0n/CorpusCookApp.git) or other scripts like [CorpusCookApp/human_in_loop_client/paper_reader.py](Scientific Paper Reader), that tries t get the text out of pdfs and other formats and feeds it to the prediction server.

The server starts load the allennlp model and waits for commands, that are defined in [annotation_protocol.py](https://github.com/c0ntradicti0n/CorpusCook/blob/master/human_in_loop_SandC/human_in_loop_client/annotation_protocol.py)
It's a twisted AMP server, that compresses JSON to keep the packages small enough.




```
loading archive file human_in_loop_server/ai_models/models/model.tar.gz
extracting archive file human_in_loop_server/ai_models/models/model.tar.gz to temp dir /tmp/tmph9wvbpfh
type = default
Loading token dictionary from /tmp/tmph9wvbpfh/vocabulary.
instantiating class <class 'allennlp.models.model.Model'> from params {'encoder': {'hidden_size': 78, 'input_size': 309, 'num_layers': 3, 'type': 'stacked_bidirectional_lstm'}, 'include_start_end_transitions': False, 'feedforward': {'activations': 'relu', 'hidden_dims': [156, 156, 156, 156, 156, 156, 156], 'input_dim': 156, 'num_layers': 7}, 'label_encoding': 'BIOUL', 'constrain_crf_decoding': True, 'dropout': 0.5, 'regularizer': [['scalar_parameters', {'alpha': 0.1, 'type': 'l2'}]], 'type': 'attentive_crf_tagger', 'calculate_span_f1': True, 'text_field_embedder': {'token_embedders': {'token_characters': {'embedding': {'embedding_dim': 9}, 'encoder': {'conv_layer_activation': 'relu', 'embedding_dim': 9, 'ngram_filter_sizes': [3], 'num_filters': 53, 'type': 'cnn'}, 'type': 'character_encoding'}, 'elmo': {'dropout': 0, 'do_layer_norm': False, 'type': 'elmo_token_embedder', 'weight_file': '/tmp/tmph9wvbpfh/fta/model.text_field_embedder.token_embedders.elmo.weight_file', 'options_file': '/tmp/tmph9wvbpfh/fta/model.text_field_embedder.token_embedders.elmo.options_file'}}}} and extras {'vocab'}
model.type = attentive_crf_tagger
instantiating class <class 'attention_please_tagger.attention_please_tagger.AttentiveCrfTagger'> from params {'encoder': {'hidden_size': 78, 'input_size': 309, 'num_layers': 3, 'type': 'stacked_bidirectional_lstm'}, 'include_start_end_transitions': False, 'feedforward': {'activations': 'relu', 'hidden_dims': [156, 156, 156, 156, 156, 156, 156], 'input_dim': 156, 'num_layers': 7}, 'label_encoding': 'BIOUL', 'constrain_crf_decoding': True, 'dropout': 0.5, 'regularizer': [['scalar_parameters', {'alpha': 0.1, 'type': 'l2'}]], 'calculate_span_f1': True, 'text_field_embedder': {'token_embedders': {'token_characters': {'embedding': {'embedding_dim': 9}, 'encoder': {'conv_layer_activation': 'relu', 'embedding_dim': 9, 'ngram_filter_sizes': [3], 'num_filters': 53, 'type': 'cnn'}, 'type': 'character_encoding'}, 'elmo': {'dropout': 0, 'do_layer_norm': False, 'type': 'elmo_token_embedder', 'weight_file': '/tmp/tmph9wvbpfh/fta/model.text_field_embedder.token_embedders.elmo.weight_file', 'options_file': '/tmp/tmph9wvbpfh/fta/model.text_field_embedder.token_embedders.elmo.options_file'}}}} and extras {'vocab'}
instantiating class <class 'allennlp.modules.text_field_embedders.text_field_embedder.TextFieldEmbedder'> from params {'token_embedders': {'token_characters': {'embedding': {'embedding_dim': 9}, 'encoder': {'conv_layer_activation': 'relu', 'embedding_dim': 9, 'ngram_filter_sizes': [3], 'num_filters': 53, 'type': 'cnn'}, 'type': 'character_encoding'}, 'elmo': {'dropout': 0, 'do_layer_norm': False, 'type': 'elmo_token_embedder', 'weight_file': '/tmp/tmph9wvbpfh/fta/model.text_field_embedder.token_embedders.elmo.weight_file', 'options_file': '/tmp/tmph9wvbpfh/fta/model.text_field_embedder.token_embedders.elmo.options_file'}}} and extras {'vocab'}
model.text_field_embedder.type = basic
model.text_field_embedder.embedder_to_indexer_map = None
model.text_field_embedder.allow_unmatched_keys = False
instantiating class <class 'allennlp.modules.token_embedders.token_embedder.TokenEmbedder'> from params {'embedding': {'embedding_dim': 9}, 'encoder': {'conv_layer_activation': 'relu', 'embedding_dim': 9, 'ngram_filter_sizes': [3], 'num_filters': 53, 'type': 'cnn'}, 'type': 'character_encoding'} and extras {'vocab'}
model.text_field_embedder.token_embedders.token_characters.type = character_encoding
model.text_field_embedder.token_embedders.token_characters.embedding.num_embeddings = None
model.text_field_embedder.token_embedders.token_characters.embedding.vocab_namespace = token_characters
model.text_field_embedder.token_embedders.token_characters.embedding.embedding_dim = 9
model.text_field_embedder.token_embedders.token_characters.embedding.pretrained_file = None
model.text_field_embedder.token_embedders.token_characters.embedding.projection_dim = None
model.text_field_embedder.token_embedders.token_characters.embedding.trainable = True
model.text_field_embedder.token_embedders.token_characters.embedding.padding_index = None
model.text_field_embedder.token_embedders.token_characters.embedding.max_norm = None
model.text_field_embedder.token_embedders.token_characters.embedding.norm_type = 2.0
model.text_field_embedder.token_embedders.token_characters.embedding.scale_grad_by_freq = False
model.text_field_embedder.token_embedders.token_characters.embedding.sparse = False
instantiating class <class 'allennlp.modules.seq2vec_encoders.seq2vec_encoder.Seq2VecEncoder'> from params {'conv_layer_activation': 'relu', 'embedding_dim': 9, 'ngram_filter_sizes': [3], 'num_filters': 53, 'type': 'cnn'} and extras set()
model.text_field_embedder.token_embedders.token_characters.encoder.type = cnn
instantiating class <class 'allennlp.modules.seq2vec_encoders.cnn_encoder.CnnEncoder'> from params {'conv_layer_activation': 'relu', 'embedding_dim': 9, 'ngram_filter_sizes': [3], 'num_filters': 53} and extras set()
model.text_field_embedder.token_embedders.token_characters.encoder.embedding_dim = 9
model.text_field_embedder.token_embedders.token_characters.encoder.num_filters = 53
model.text_field_embedder.token_embedders.token_characters.encoder.ngram_filter_sizes = [3]
model.text_field_embedder.token_embedders.token_characters.encoder.conv_layer_activation = relu
model.text_field_embedder.token_embedders.token_characters.encoder.output_dim = None
model.text_field_embedder.token_embedders.token_characters.dropout = 0.0
instantiating class <class 'allennlp.modules.token_embedders.token_embedder.TokenEmbedder'> from params {'dropout': 0, 'do_layer_norm': False, 'type': 'elmo_token_embedder', 'weight_file': '/tmp/tmph9wvbpfh/fta/model.text_field_embedder.token_embedders.elmo.weight_file', 'options_file': '/tmp/tmph9wvbpfh/fta/model.text_field_embedder.token_embedders.elmo.options_file'} and extras {'vocab'}
model.text_field_embedder.token_embedders.elmo.type = elmo_token_embedder
model.text_field_embedder.token_embedders.elmo.options_file = /tmp/tmph9wvbpfh/fta/model.text_field_embedder.token_embedders.elmo.options_file
model.text_field_embedder.token_embedders.elmo.weight_file = /tmp/tmph9wvbpfh/fta/model.text_field_embedder.token_embedders.elmo.weight_file
model.text_field_embedder.token_embedders.elmo.requires_grad = False
model.text_field_embedder.token_embedders.elmo.do_layer_norm = False
model.text_field_embedder.token_embedders.elmo.dropout = 0
model.text_field_embedder.token_embedders.elmo.namespace_to_cache = None
model.text_field_embedder.token_embedders.elmo.projection_dim = None
model.text_field_embedder.token_embedders.elmo.scalar_mix_parameters = None
Initializing ELMo
instantiating class <class 'allennlp.modules.seq2seq_encoders.seq2seq_encoder.Seq2SeqEncoder'> from params {'hidden_size': 78, 'input_size': 309, 'num_layers': 3, 'type': 'stacked_bidirectional_lstm'} and extras {'vocab'}
model.encoder.type = stacked_bidirectional_lstm
model.encoder.batch_first = True
model.encoder.stateful = False
Converting Params object to dict; logging of default values will not occur when dictionary parameters are used subsequently.
CURRENTLY DEFINED PARAMETERS: 
model.encoder.hidden_size = 78
model.encoder.input_size = 309
model.encoder.num_layers = 3
model.label_namespace = labels
instantiating class <class 'allennlp.modules.feedforward.FeedForward'> from params {'activations': 'relu', 'hidden_dims': [156, 156, 156, 156, 156, 156, 156], 'input_dim': 156, 'num_layers': 7} and extras {'vocab'}
model.feedforward.input_dim = 156
model.feedforward.num_layers = 7
model.feedforward.hidden_dims = [156, 156, 156, 156, 156, 156, 156]
model.feedforward.hidden_dims = [156, 156, 156, 156, 156, 156, 156]
model.feedforward.activations = relu
model.feedforward.dropout = 0.0
model.label_encoding = BIOUL
model.include_start_end_transitions = False
model.attention = None
model.constrain_crf_decoding = True
model.calculate_span_f1 = True
model.dropout = 0.5
model.verbose_metrics = False
model.regularizer.0.1.type = l2
Initializing parameters
Done initializing parameters; the following parameters are using their default initialization from their code
   _feedforward._linear_layers.0.bias
   _feedforward._linear_layers.0.weight
   _feedforward._linear_layers.1.bias
   _feedforward._linear_layers.1.weight
   _feedforward._linear_layers.2.bias
   _feedforward._linear_layers.2.weight
   _feedforward._linear_layers.3.bias
   _feedforward._linear_layers.3.weight
   _feedforward._linear_layers.4.bias
   _feedforward._linear_layers.4.weight
   _feedforward._linear_layers.5.bias
   _feedforward._linear_layers.5.weight
   _feedforward._linear_layers.6.bias
   _feedforward._linear_layers.6.weight
   crf._constraint_mask
   crf.transitions
   encoder._module.backward_layer_0.input_linearity.weight
   encoder._module.backward_layer_0.state_linearity.bias
   encoder._module.backward_layer_0.state_linearity.weight
   encoder._module.backward_layer_1.input_linearity.weight
   encoder._module.backward_layer_1.state_linearity.bias
   encoder._module.backward_layer_1.state_linearity.weight
   encoder._module.backward_layer_2.input_linearity.weight
   encoder._module.backward_layer_2.state_linearity.bias
   encoder._module.backward_layer_2.state_linearity.weight
   encoder._module.forward_layer_0.input_linearity.weight
   encoder._module.forward_layer_0.state_linearity.bias
   encoder._module.forward_layer_0.state_linearity.weight
   encoder._module.forward_layer_1.input_linearity.weight
   encoder._module.forward_layer_1.state_linearity.bias
   encoder._module.forward_layer_1.state_linearity.weight
   encoder._module.forward_layer_2.input_linearity.weight
   encoder._module.forward_layer_2.state_linearity.bias
   encoder._module.forward_layer_2.state_linearity.weight
   tag_projection_layer._module.bias
   tag_projection_layer._module.weight
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._elmo_lstm.backward_layer_0.input_linearity.weight
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._elmo_lstm.backward_layer_0.state_linearity.bias
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._elmo_lstm.backward_layer_0.state_linearity.weight
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._elmo_lstm.backward_layer_0.state_projection.weight
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._elmo_lstm.backward_layer_1.input_linearity.weight
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._elmo_lstm.backward_layer_1.state_linearity.bias
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._elmo_lstm.backward_layer_1.state_linearity.weight
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._elmo_lstm.backward_layer_1.state_projection.weight
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._elmo_lstm.forward_layer_0.input_linearity.weight
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._elmo_lstm.forward_layer_0.state_linearity.bias
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._elmo_lstm.forward_layer_0.state_linearity.weight
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._elmo_lstm.forward_layer_0.state_projection.weight
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._elmo_lstm.forward_layer_1.input_linearity.weight
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._elmo_lstm.forward_layer_1.state_linearity.bias
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._elmo_lstm.forward_layer_1.state_linearity.weight
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._elmo_lstm.forward_layer_1.state_projection.weight
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._token_embedder._char_embedding_weights
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._token_embedder._highways._layers.0.bias
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._token_embedder._highways._layers.0.weight
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._token_embedder._projection.bias
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._token_embedder._projection.weight
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._token_embedder.char_conv_0.bias
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._token_embedder.char_conv_0.weight
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._token_embedder.char_conv_1.bias
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._token_embedder.char_conv_1.weight
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._token_embedder.char_conv_2.bias
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._token_embedder.char_conv_2.weight
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._token_embedder.char_conv_3.bias
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._token_embedder.char_conv_3.weight
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._token_embedder.char_conv_4.bias
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._token_embedder.char_conv_4.weight
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._token_embedder.char_conv_5.bias
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._token_embedder.char_conv_5.weight
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._token_embedder.char_conv_6.bias
   text_field_embedder.token_embedder_elmo._elmo._elmo_lstm._token_embedder.char_conv_6.weight
   text_field_embedder.token_embedder_elmo._elmo.scalar_mix_0.gamma
   text_field_embedder.token_embedder_elmo._elmo.scalar_mix_0.scalar_parameters.0
   text_field_embedder.token_embedder_elmo._elmo.scalar_mix_0.scalar_parameters.1
   text_field_embedder.token_embedder_elmo._elmo.scalar_mix_0.scalar_parameters.2
   text_field_embedder.token_embedder_token_characters._embedding._module.weight
   text_field_embedder.token_embedder_token_characters._encoder._module.conv_layer_0.bias
   text_field_embedder.token_embedder_token_characters._encoder._module.conv_layer_0.weight
instantiating class <class 'allennlp.data.dataset_readers.dataset_reader.DatasetReader'> from params {'coding_scheme': 'BIOUL', 'tag_label': 'ner', 'token_indexers': {'elmo': {'type': 'elmo_characters'}, 'token_characters': {'min_padding_length': 3, 'type': 'characters'}}, 'type': 'conll2003'} and extras set()
dataset_reader.type = conll2003
instantiating class <class 'allennlp.data.dataset_readers.conll2003.Conll2003DatasetReader'> from params {'coding_scheme': 'BIOUL', 'tag_label': 'ner', 'token_indexers': {'elmo': {'type': 'elmo_characters'}, 'token_characters': {'min_padding_length': 3, 'type': 'characters'}}} and extras set()
instantiating class allennlp.data.token_indexers.token_indexer.TokenIndexer from params {'type': 'elmo_characters'} and extras set()
dataset_reader.token_indexers.elmo.type = elmo_characters
instantiating class allennlp.data.token_indexers.elmo_indexer.ELMoTokenCharactersIndexer from params {} and extras set()
dataset_reader.token_indexers.elmo.namespace = elmo_characters
dataset_reader.token_indexers.elmo.tokens_to_add = None
dataset_reader.token_indexers.elmo.token_min_padding_length = 0
instantiating class allennlp.data.token_indexers.token_indexer.TokenIndexer from params {'min_padding_length': 3, 'type': 'characters'} and extras set()
dataset_reader.token_indexers.token_characters.type = characters
instantiating class allennlp.data.token_indexers.token_characters_indexer.TokenCharactersIndexer from params {'min_padding_length': 3} and extras set()
dataset_reader.token_indexers.token_characters.namespace = token_characters
dataset_reader.token_indexers.token_characters.start_tokens = None
dataset_reader.token_indexers.token_characters.end_tokens = None
dataset_reader.token_indexers.token_characters.min_padding_length = 3
dataset_reader.token_indexers.token_characters.token_min_padding_length = 0
dataset_reader.tag_label = ner
dataset_reader.feature_labels = ()
dataset_reader.lazy = False
dataset_reader.coding_scheme = BIOUL
dataset_reader.label_namespace = labels
Server started, waiting for commands
```

When a command was called like making predictions, the server makes this prediction and sends it back.
So, when using my difference-between-model on some Adoph Grünbaum statement over Aristotle distinguishing knowing-why and knowing-how, it may print:

```buildoutcfg
SENTENCE Specifically , he distinguished between know-how ( the sort of knowledge which the craftsman and the engineer possess ) and what we might call know-why or demonstrative understanding ( which the scientist alone possesses ) . A shipbuilder , for instance , knows how to form pieces of wood together so as to make a seaworthy vessel ; but he does not have , and has no need for , a syllogistic , causal demonstration based on the primary principles or first causes of things . Thus , he needs to know that wood , when properly sealed , floats ; but he need not be able to show by virtue of what principles and causes wood has this property of buoyancy .
[[(360, 'O'), (361, 'O'), (362, 'O'), (363, 'O'), (364, 'O')],
 [(365, 'B-SUBJECT'),
  (366, 'I-CONTRAST'),
  (367, 'I-CONTRAST'),
  (368, 'I-CONTRAST'),
  (369, 'I-CONTRAST'),
  (370, 'I-CONTRAST'),
  (371, 'I-CONTRAST'),
  (372, 'I-CONTRAST'),
  (373, 'I-CONTRAST'),
  (374, 'I-CONTRAST'),
  (375, 'I-CONTRAST'),
  (376, 'I-CONTRAST'),
  (377, 'I-CONTRAST'),
  (378, 'I-CONTRAST'),
  (379, 'O'),
  (380, 'O'),
  (381, 'O'),
  (382, 'O'),
  (383, 'O')],
 [(384, 'B-SUBJECT'),
  (385, 'I-CONTRAST'),
  (386, 'I-CONTRAST'),
  (387, 'I-CONTRAST'),
  (388, 'I-CONTRAST'),
  (389, 'I-CONTRAST'),
  (390, 'I-CONTRAST'),
  (391, 'I-CONTRAST'),
  (392, 'I-CONTRAST'),
  (393, 'I-CONTRAST'),
  (394, 'I-CONTRAST'),
  (395, 'O'),
  (396, 'O'),
  (397, 'O'),
  (398, 'O'),
  (399, 'O'),
  (400, 'O'),
  (401, 'O'),
  (402, 'O'),
  (403, 'O'),
  (404, 'O'),
  (405, 'O'),
  (406, 'O'),
  (407, 'O'),
  (408, 'O'),
  (409, 'O'),
  (410, 'O'),
  (411, 'O'),
  (412, 'O'),
  (413, 'O'),
  (414, 'O'),
  (415, 'O'),
  (416, 'O'),
  (417, 'O'),
  (418, 'O'),
  (419, 'O'),
  (420, 'O'),
  (421, 'O'),
  (422, 'O'),
  (423, 'O'),
  (424, 'O'),
  (425, 'O'),
  (426, 'O'),
  (427, 'O'),
  (428, 'O'),
  (429, 'O'),
  (430, 'O'),
  (431, 'O'),
  (432, 'O'),
  (433, 'O'),
  (434, 'O'),
  (435, 'O'),
  (436, 'O'),
  (437, 'O'),
  (438, 'O'),
  (439, 'O'),
  (440, 'O'),
  (441, 'O'),
  (442, 'O'),
  (443, 'O'),
  (444, 'O'),
  (445, 'O'),
  (446, 'O'),
  (447, 'O'),
  (448, 'O'),
  (449, 'O'),
  (450, 'O'),
  (451, 'O'),
  (452, 'O'),
  (453, 'O'),
  (454, 'O'),
  (455, 'O'),
  (456, 'O'),
  (457, 'O'),
  (458, 'O'),
  (459, 'O'),
  (460, 'O'),
  (461, 'O'),
  (462, 'O'),
  (463, 'O'),
  (464, 'O'),
  (465, 'O'),
  (466, 'O'),
  (467, 'O'),
  (468, 'O'),
  (469, 'O'),
  (470, 'O'),
  (471, 'O'),
  (472, 'O'),
  (473, 'O'),
  (474, 'O'),
  (475, 'O'),
  (476, 'O'),
  (477, 'O'),
  (478, 'O'),
  (479, 'O'),
  (480, 'O'),
  (481, 'O'),
  (482, 'O')]]
```