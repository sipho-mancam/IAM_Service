from password_validator import PasswordValidator

password_schema = PasswordValidator()

password_schema.min(8).max(100).has().digits().has().letters().has().symbols().has().lowercase().has().uppercase()
