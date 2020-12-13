// Third party libraries
import React from 'react';

export const SplitDiv = ({ left, right }) => (
  <div style={{ alignItems: 'center', display: 'flex' }}>
    <div style={{ margin: 'auto' }}>
      {left}
    </div>
    <div style={{ display: 'flex', flex: '1' }}>
      {right}
    </div>
  </div>
)
