const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

const cors = require('cors');
const database = require('./database');

app.use(cors());
app.use(express.json());
database.connect();

app.use('/', require('./routes/hello'));
app.use('/', require('./routes/login'));
app.use('/', require('./routes/api'));
app.use('/', require('./routes/register'));
app.use('/', require('./routes/api_admin'));

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});