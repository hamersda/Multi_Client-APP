const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const secretKey = 'a(3nfUwWn98294nd;voBAMeawJdoqLsdci3asdc49';
const key = '6uNyOfjhKw8E2WwW2WQZ2rzQh0mkrNzXzf7KNLby9Zs=';  // Replace 'YOUR_KEY_HERE' with the actual key

function decryptFernetMessage(key, encryptedMessage) {
  // Convert the key from base64 to a buffer
  const keyBuffer = Buffer.from(key, 'base64');

  // Create an initialization vector (IV) from the first 16 bytes of the encrypted message
  const iv = Buffer.from(encryptedMessage, 'base64').slice(0, 16);

  // Create a decipher object using the key and IV
  const decipher = crypto.createDecipheriv('aes-128-cbc', keyBuffer, iv);

  // Set the padding option to false since Fernet uses its own padding
  decipher.setAutoPadding(false);

  // Decrypt the message
  let decryptedMessage = decipher.update(encryptedMessage, 'base64', 'utf8');
  decryptedMessage += decipher.final('utf8');

  return decryptedMessage;
}

const Pool = require('pg').Pool;
const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'tubes',
  password: 'Admin',
  port: 5432,
});
const getUsers = (request, response) => {
  pool.query('SELECT * FROM profiles ORDER BY id_user ASC', (error, results) => {
    if (error) {
      throw error;
    }
    response.status(200).json(results.rows);
  });
};

const getUserById = (request, response) => {
  const id = parseInt(request.params.id);

  pool.query('SELECT * FROM profiles WHERE id_user = $1', [id], (error, results) => {
    if (error) {
      throw error;
    }
    response.status(200).json(results.rows);
  });
};

const createUser = (request, response) => {
  const { username, password, full_name } = request.body;

  bcrypt.hash(password, 10, (error, hashedPassword) => {
    if (error) {
      throw error;
    }

    pool.query(
      'INSERT INTO profiles (username, password, full_name) VALUES ($1, $2, $3) RETURNING *',
      [username, hashedPassword, full_name],
      (error, results) => {
        if (error) {
          response.status(400).json(`{
            "status": 400,
            "message": "User not added"
          }`);
          throw error;
        }
        response.status(201).json(`{
          "status": 201,
          "message": "User added with ID: ${results.rows[0].id_user}"
        }`); //with ID: ${results.rows[0].id}
      }
    ); 
  });
};

const updateUser = (request, response) => {
  const id = parseInt(request.params.id);
  const { username, password, full_name } = request.body;

  pool.query(
    'UPDATE profiles SET username = $1, password = $2, full_name = $3 WHERE id_user = $4',
    [username, password, full_name, id],
    (error, results) => {
      if (error) {
        throw error;
      }
      response.status(200).json(`{
        "status": 200,
        "message": "User modified with ID: ${id}"
      }`);
    }
  );
};

const deleteUser = (request, response) => {
  const id = parseInt(request.params.id);

  pool.query('DELETE FROM profiles WHERE id_user = $1', [id], (error, results) => {
    if (error) {
      throw error;
    }
    response.status(200).json(`{
      "status": 200,
      "message": "User deleted with ID: ${id}"
    }`);
  });
};

const getMessage = (request, response) => {
  pool.query('SELECT * FROM messages INNER JOIN devices USING (id_device) ORDER BY received_time DESC LIMIT 100', (error, results) => {
    if (error) {
      throw error;
    }
    response.status(200).json(results.rows);
  });
};

const getMessageById = (request, response) => {
  const id = parseInt(request.params.id);

  pool.query('SELECT * FROM messages INNER JOIN devices USING (id_device) WHERE id_message = $1', [id], (error, results) => {
    if (error) {
      throw error;
    }
    response.status(200).json(results.rows);
  });
};

const createMessage = (request, response) => {
  const { id_device, id_user, suhu } = request.body;

  pool.query(
    'INSERT INTO messages (id_device, id_user, suhu) VALUES ($1, $2, $3) RETURNING *',
    [id_device, id_user, suhu],
    (error, results) => {
      if (error) {
        throw error;
      }
      response.status(201).json(`{
        "status": 201,
        "message": "Message added with ID: ${results.rows[0].id_message}"
      }`);
    }
  );
};

const updateMessage = (request, response) => {
  const id = parseInt(request.params.id);
  const { id_device, id_user, suhu } = request.body;

  pool.query(
    'UPDATE messages SET id_device = $1, id_user = $2, suhu = $3 WHERE id_message = $4',
    [id_device, id_user, suhu, id],
    (error, results) => {
      if (error) {
        throw error;
      }
      response.status(200).json(`{
        "status": 200,
        "message": "Message modified with ID: ${ID}"
      }`);
    }
  );
};

const deleteMessage = (request, response) => {
  const id_message = parseInt(request.params.id);

  pool.query('DELETE FROM messages WHERE id_message = $1', [id_message], (error, results) => {
    if (error) {
      throw error;
    }
    response.status(200).json(`{
      "status": 200,
      "message": "Message deleted with ID: ${ID}"
    }`);
  });
};

const getDevice = (request, response) => {
  pool.query('SELECT * FROM devices ORDER BY id_device ASC', (error, results) => {
    if (error) {
      throw error;
    }
    response.status(200).json(results.rows);
  });
};

const getDeviceById = (request, response) => {
  const id = parseInt(request.params.id);

  pool.query('SELECT * FROM devices WHERE id_device = $1', [id], (error, results) => {
    if (error) {
      throw error;
    }
    response.status(200).json(results.rows);
  });
};

const createDevice = (request, response) => {
  const { device_name, room } = request.body;

  pool.query(
    'INSERT INTO devices (device_name, room) VALUES ($1, $2) RETURNING *',
    [device_name, room],
    (error, results) => {
      if (error) {
        throw error;
      }
      response.status(201).json(`{
        "status": 201,
        "message": "Device added with ID: ${results.rows[0].id_device}"
      }`); //with ID: ${results.rows[0].id}
    }
  );
};

const updateDevice = (request, response) => {
  const id = parseInt(request.params.id);
  const { device_name, room } = request.body;

  pool.query(
    'UPDATE devices SET device_name = $1, room = $2 WHERE id_device = $3',
    [device_name, room, id],
    (error, results) => {
      if (error) {
        throw error;
      }
      response.status(200).json(`{
        "status": 200,
        "message": "Device updated with ID: ${ID}"
      }`);
    }
  );
};

const deleteDevice = (request, response) => {
  const id = parseInt(request.params.id);

  pool.query('DELETE FROM devices WHERE id_device = $1', [id], (error, results) => {
    if (error) {
      throw error;
    }
    response.status(200).json(`{
      "status": 200,
      "message": "Device deleted with ID: ${ID}"
    }`);
  });
};

const findUserByUsername = async (username) => {
  const query = 'SELECT id_user FROM profiles WHERE username = $1;';
  const values = [username];

  try {
    const { rows } = await pool.query(query, values);

    if (rows.length === 0) {
      // User not found
      return null;
    }

    // User found
    return rows[0];
  } catch (error) {
    // Handle error
    console.error(error);
    throw error;
  }
};

const checkPassword = (request, response) => {
  const { username, password } = request.body;

  try {
    const user = findUserByUsername(username);
    // console.log(user);

    if (!user) {
      // User not found
      return response.status(404).json({
        status: 404,
        message: 'User not found',
      });
    }

    // Fetch the hashed password from the database
    pool.query('SELECT password FROM profiles WHERE username = $1', [username], async (error, results) => {
      if (error) {
        throw error;
      }

      const hashedPass = results.rows[0].password;

      // Compare the entered password with the hashed password
      const isPasswordMatch = await bcrypt.compare(password, hashedPass);

      if (!isPasswordMatch) {
        // Password does not match
        return response.status(401).json({
          status: 401,
          message: 'Password does not match',
        });
      }

      // Password matches, generate a JWT token
      const token = jwt.sign({username}, secretKey, { algorithm: 'HS256', expiresIn: '1h' });

      return response.status(200).json({
        status: 200,
        id_user: user.id_user,
        message: 'Password match',
        token: token,
      });
    });
  } catch (error) {
    // Handle error
    console.error(error);
    throw error;
  }
};

// Middleware function to verify the token
const authenticateToken = (request, response, next) => {
  const token = request.headers.authorization.split(' ')[1];

  if (!token) {
    return response.status(401).json({
      status: 401,
      message: 'No token provided',
    });
  }

  jwt.verify(token, secretKey, {algorithm: 'HS256'},(error, decoded) => {
    if (error) {
      
      console.error(error);
      return response.status(403).json({
        status: 403,
        message: 'Invalid token',
      });
    }

    // Token is valid, store the decoded information in the request object
    
    request.user = decoded;

    // Proceed to the next middleware or route handler
    next();
  });
};


module.exports = {
  getUsers,
  getUserById,
  createUser,
  updateUser,
  deleteUser,
  getMessage,
  getMessageById,
  createMessage,
  updateMessage,
  deleteMessage,  
  getDevice,
  getDeviceById,
  createDevice,
  updateDevice,
  deleteDevice, 
  checkPassword,
  authenticateToken,
};