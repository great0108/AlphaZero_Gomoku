import numpy as np

def get_equi_data(self, play_data):
        """augment the data set by rotation and flipping
        play_data: [(state, mcts_prob, winner_z), ..., ...]
        """
        extend_data = []
        for state, mcts_porb, winner in play_data:
            for i in [1, 2, 3, 4]:
                # rotate counterclockwise
                equi_state = np.array([np.rot90(s, i) for s in state])
                equi_mcts_prob = np.rot90(
                    mcts_porb.reshape(state.shape[1], state.shape[2]), i)
                extend_data.append((equi_state,
                                    equi_mcts_prob.flatten(),
                                    winner))
                # flip horizontally
                equi_state = np.array([np.fliplr(s) for s in equi_state])
                equi_mcts_prob = np.fliplr(equi_mcts_prob)
                extend_data.append((equi_state,
                                    equi_mcts_prob.flatten(),
                                    winner))
        return extend_data

state = np.arange(36).reshape(4,3,3)
mcts_prob = np.arange(1, 10).reshape(1,9)
winner = [1]
data = [(state, mcts_prob, winner), (state, mcts_prob, winner)]
datas = get_equi_data(data)
for a in datas:
    print(a)

# a = np.arange(9).reshape(3,3)
# print(a)