---
title: Create an Array Input or Tag input feature with React and Mui
date: 2023-11-30
tags: react mui
categoris: Programming
---

The idea is to implement this feature with Mui's `TextField` component, and display the tags/array in it's `startAdornment`.

```javascript
import { useState } from "react";
import "./styles.css";
import { ArrayInput } from "./ArrayInput";
import CorporateFareTwoToneIcon from "@mui/icons-material/CorporateFareTwoTone";

export default function App() {
  const [domains, setDomains] = useState(["a.com", "b.com"]);

  return (
    <div className="App">
      <ArrayInput
        AdornmentIcon={CorporateFareTwoToneIcon}
        values={domains}
        label="Domain Aliases"
        onDelete={(value, index) =>
          setDomains(domains.filter((name, i) => i !== index))
        }
        onAdd={(value) => setDomains([...domains, value])}
      />
    </div>
  );
}
```

```javascript
// ArrayInput.js
import { Box, Typography, TextField, Button, InputAdornment, Stack } from '@mui/material';
import CancelIcon from '@mui/icons-material/Cancel';
import { useState } from 'react';

const ArrayFieldValue = ({ value, index, onDelete }) => {
  return (
    <Box
      component="span"
      sx={{
        display: 'inline-flex',
        backgroundColor: '#ffffff',
        border: '1px solid #D9D9D9',
        px: 0.5,
        py: 0,
        fontWeight: 500,
        borderRadius: '4px',
        alignItems: 'center',
        mr: 0.5,
        '& .btn': {
          ml: 1
        }
      }}
    >
      <Typography variant="body2">{value}</Typography>
      <CancelIcon
        className="btn"
        stroke={1.5}
        size="1rem"
        sx={{ color: '#757575', width: '0.6em', height: '0.6em', cursor: 'pointer' }}
        onClick={(event) => {
          event.stopPropagation();
          if (onDelete) onDelete(value, index);
        }}
      />
    </Box>
  );
};

export const ArrayInput = ({ values = [], AdornmentIcon, label, onDelete, onAdd }) => {
  const totalCount = values.length;
  const [expanded, setExpanded] = useState(false);
  const displayValues = values.slice(0, expanded ? totalCount : 3);
  const displayValuesCount = displayValues.length;

  const [inputValue, setInputValue] = useState('');
  const handleKeyInput = async (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      if (inputValue) {
        if (onAdd) onAdd(inputValue);
        setInputValue('');
      }
    }
  };

  return (
    <TextField
      fullWidth
      label={label}
      size="small"
      sx={{
        '& input': {
          width: 'auto',
          minWidth: '1em'
        }
      }}
      value={inputValue}
      onChange={(event) => setInputValue(event.target.value)}
      onKeyDown={handleKeyInput}
      InputProps={{
        startAdornment: (
          <InputAdornment position="start" sx={{ height: 'auto', maxHeight: 'inherit', overflowX: 'auto' }}>
            {AdornmentIcon && <AdornmentIcon sx={{ width: '1rem', height: '1rem' }} />}
            {displayValuesCount > 0 && (
              <Stack direction="row" gap={1} sx={{ flexWrap: 'wrap', m: '14px' }}>
                {displayValues.map((value, index) => {
                  return <ArrayFieldValue value={value} index={index} key={index} onDelete={onDelete} />;
                })}
                {totalCount > 3 && (
                  <Button variant="text" size="small" onClick={() => setExpanded((prev) => !prev)}>
                    {expanded ? 'Show less' : `+${totalCount - 3} more`}
                  </Button>
                )}
              </Stack>
            )}
          </InputAdornment>
        )
      }}
    />
  );
};
```

codesandbox: https://codesandbox.io/p/sandbox/lively-night-y279n3

See https://blog.theashishmaurya.me/how-to-create-a-tag-input-feature-in-reactjs-and-material-ui