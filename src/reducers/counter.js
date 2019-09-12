import {
  DECREMENT,
  DECREMENT_REQUESTED,
  INCREMENT,
  INCREMENT_REQUESTED
} from '../actions/counter';

const initialState = {
  count: 0,
  isIncrementing: false,
  isDecrementing: false
};

const counter = (state = initialState, action) => {
  switch (action.type) {
    case DECREMENT:
      return {
        ...state,
        count: state.count - 1,
        isDecrementing: !state.isDecrementing
      };

    case DECREMENT_REQUESTED:
      return {
        ...state,
        isDecrementing: true
      };

    case INCREMENT:
      return {
        ...state,
        count: state.count + 1,
        isIncrementing: !state.isIncrementing
      };
    case INCREMENT_REQUESTED:
      return {
        ...state,
        isIncrementing: true
      };
    default:
      return state;
  }
};

export default counter