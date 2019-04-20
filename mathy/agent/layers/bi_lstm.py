import tensorflow as tf


def BiLSTM(units, name="bi_lstm_stack", state=True):
    """Bi-directional LSTM for processing input context vectors"""

    def func(input_layer):
        forward_layer = tf.keras.layers.LSTM(
            units, return_sequences=True, return_state=True, name="lstm/forward"
        )
        backward_layer = tf.keras.layers.LSTM(
            units,
            return_sequences=True,
            go_backwards=True,
            return_state=True,
            name="lstm/backward",
        )
        lstm_fwd, state_h_fwd, state_c_fwd = forward_layer(input_layer)
        lstm_bwd, state_h_bwd, state_c_bwd = backward_layer(input_layer)

        return (
            tf.keras.layers.Add(name=f"{name}_states")([state_h_fwd, state_h_bwd]),
            tf.keras.layers.Concatenate(name=name)([lstm_fwd, lstm_bwd, input_layer]),
        )

    return func