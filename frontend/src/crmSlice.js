import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  messages: [],
};

const crmSlice = createSlice({
  name: "crm",
  initialState,
  reducers: {
    addMessage: (state, action) => {
      state.messages.push(action.payload);
    },
    clearMessages: (state) => {
      state.messages = [];
    },
  },
});

export const { addMessage, clearMessages } = crmSlice.actions;
export default crmSlice.reducer;