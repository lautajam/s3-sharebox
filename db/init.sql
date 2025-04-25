-- Crear las tablas
CREATE TABLE IF NOT EXISTS roles (
  role_id SERIAL PRIMARY KEY,
  role_name VARCHAR(255),
  role_description TEXT,
  can_create_files BOOLEAN,
  can_create_folders BOOLEAN
);

CREATE TABLE IF NOT EXISTS users (
  user_id SERIAL PRIMARY KEY,
  full_name VARCHAR(255),
  username VARCHAR(255),
  password VARCHAR(255),
  role_id INT,
  created_at TIMESTAMP DEFAULT current_timestamp,
  FOREIGN KEY (role_id) REFERENCES roles(role_id)
);

CREATE TABLE IF NOT EXISTS tags (
  tag_id SERIAL PRIMARY KEY,
  tag_name VARCHAR(255),
  tag_description TEXT
);

CREATE TABLE IF NOT EXISTS folders (
  folder_id SERIAL PRIMARY KEY,
  folder_name VARCHAR(255),
  parent_folder_id INT,
  FOREIGN KEY (parent_folder_id) REFERENCES folders(folder_id)
);

CREATE TABLE IF NOT EXISTS files (
  file_id SERIAL PRIMARY KEY,
  file_name VARCHAR(255),
  file_metadata JSONB,
  file_type VARCHAR(255),
  s3_url VARCHAR(255),
  folder_id INT,
  uploaded_at TIMESTAMP DEFAULT current_timestamp,
  FOREIGN KEY (folder_id) REFERENCES folders(folder_id)
);

CREATE TABLE IF NOT EXISTS file_tag (
  file_id INT,
  tag_id INT,
  PRIMARY KEY (file_id, tag_id),
  FOREIGN KEY (file_id) REFERENCES files(file_id),
  FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
);

CREATE TABLE IF NOT EXISTS folder_tag (
  folder_id INT,
  tag_id INT,
  PRIMARY KEY (folder_id, tag_id),
  FOREIGN KEY (folder_id) REFERENCES folders(folder_id),
  FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
);

CREATE TABLE IF NOT EXISTS folder_role (
  folder_id INT,
  role_id INT,
  access_level VARCHAR(255),
  PRIMARY KEY (folder_id, role_id),
  FOREIGN KEY (folder_id) REFERENCES folders(folder_id),
  FOREIGN KEY (role_id) REFERENCES roles(role_id)
);

CREATE TABLE IF NOT EXISTS file_role (
  file_id INT,
  role_id INT,
  access_level VARCHAR(255),
  PRIMARY KEY (file_id, role_id),
  FOREIGN KEY (file_id) REFERENCES files(file_id),
  FOREIGN KEY (role_id) REFERENCES roles(role_id)
);

-- Inserción de data básica
INSERT INTO roles (role_name, role_description, can_create_files, can_create_folders)
VALUES
('admin', 'Administrator role with full access', TRUE, TRUE),
('user', 'Regular user role with limited access', TRUE, FALSE),
('guest', 'Guest role with read-only access', FALSE, FALSE);

INSERT INTO users (full_name, username, password, role_id)
VALUES
('Admin-User', 'superadmin', '$2b$12$sVeMF86j.ppCWTN4iaEshOtW6j46UjVF91sijXyHZIuNx2kxTK.Te', 1);