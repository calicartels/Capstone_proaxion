# Change Machine Part Component

This component is part of the MTC (Machine Tool Configuration) application. It is designed to allow users to select and modify machine parts based on their specific requirements.

## Features

- Dynamic rendering of machine part options.
- Integration with user selections to customize the configuration process.
- Responsive design for seamless usage across devices.

## Usage

Import the component into your React application:

```tsx
import ChangeMachinePart from './components/change_machine_part/ChangeMachinePart';

function App() {
  return (
    <div>
      <ChangeMachinePart />
    </div>
  );
}

export default App;
```

## Props

The `ChangeMachinePart` component accepts the following props:

| Prop Name       | Type     | Description                                   |
|------------------|----------|-----------------------------------------------|
| `machineParts`   | `Array`  | List of machine parts to display.            |
| `onPartChange`   | `Function` | Callback function triggered on part change. |
