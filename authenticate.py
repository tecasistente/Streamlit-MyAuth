import jwt
import streamlit as st
from datetime import datetime, timedelta
import extra_streamlit_components as stx
import database as db
import bcrypt


"""from .hasher import Hasher
from .validator import Validator
from .utils import generate_random_pw

from .exceptions import CredentialsError, ForgotError, RegisterError, ResetError, UpdateError
"""


class Authenticate:
    """
    This class will create login, logout, register user, reset password, forgot password, 
    forgot username, and modify user details widgets.
    """

    def __init__(self, cookie_name: str, key: str,  cookie_expiry_days: float = 30.0,):
        """
        Create a new instance of "Authenticate".

        Parameters
        ----------
        credentials: dict
            The dictionary of username, passwords, and email and role.
        cookie_name: str
            The name of the JWT cookie stored on the client's browser for passwordless reauthentication.
        key: str
            The key to be used for hashing the signature of the JWT cookie.
        cookie_expiry_days: float
            The number of days before the cookie expires on the client's browser.
        """
        self.username = None
        self.password=None
        self.email = None
        self.role = None
        self.cookie_name = cookie_name
        self.key = key
        self.cookie_expiry_days = cookie_expiry_days
        self.cookie_manager = stx.CookieManager()

        if 'email' not in st.session_state:
            st.session_state['email'] = None
        if 'authentication_status' not in st.session_state:
            st.session_state['authentication_status'] = None
        if 'username' not in st.session_state:
            st.session_state['username'] = None
        if 'role' not in st.session_state:
            st.session_state['role'] = None
        if 'logout' not in st.session_state:
            st.session_state['logout'] = None

    def _token_encode(self) -> str:
        """
        Encodes the contents of the reauthentication cookie.

        Returns
        -------
        str
            The JWT cookie for passwordless reauthentication.
        """
        return jwt.encode({'email': st.session_state['email'],
                           'username': st.session_state['username'],
                           'role': st.session_state['role'],
                           'exp_date': self.exp_date}, self.key, algorithm='HS256')

    def _token_decode(self) -> str:
        """
        Decodes the contents of the reauthentication cookie.

        Returns
        -------
        str
            The decoded JWT cookie for passwordless reauthentication.
        """
        try:
            return jwt.decode(self.token, self.key, algorithms=['HS256'])
        except:
            return False

    def _set_exp_date(self) -> str:
        """
        Creates the reauthentication cookie's expiry date.

        Returns
        -------
        str
            The JWT cookie's expiry timestamp in Unix epoch.
        """
        return (datetime.utcnow() + timedelta(days=self.cookie_expiry_days)).timestamp()
    
    def _check_cookie(self):
        """
        Checks the validity of the reauthentication cookie.
        """
        self.token = self.cookie_manager.get(self.cookie_name)
        if self.token is not None:
            self.token = self._token_decode()
            if self.token is not False:
                if not st.session_state['logout']:
                    if self.token['exp_date'] > datetime.utcnow().timestamp():
                        if 'email' and 'username'and 'role' in self.token:
                            st.session_state['email'] = self.token['email']
                            st.session_state['role'] = self.token['role']
                            st.session_state['username'] = self.token['username']
                            st.session_state['authentication_status'] = True

    def _hash(self, password: str) -> str:
        """
        Hashes the plain text password.

        Parameters
        ----------
        password: str
            The plain text password to be hashed.
        Returns
        -------
        str
            The hashed password.
        """
        
        bytePwd = password.encode('utf-8')
        salt = bcrypt.gensalt()


        return bcrypt.hashpw(bytePwd, salt).decode()

    def _check_credentials(self) -> bool:
        """
        Checks the validity of the entered credentials.

        Parameters
        ----------
        inplace: bool
            Inplace setting, True: authentication status will be stored in session state, 
            False: authentication status will be returned as bool.
        Returns
        -------
        bool
            Validity of entered credentials.
        """
        user = db.get_user(self.username)
        if user != None and db.check_password(self.username, self.password):
            self.email=user["email"]
            self.role=user["role"]

            st.session_state["username"] = user["username"]
            st.session_state["email"] = user["email"]
            st.session_state['role'] = user["role"]
            self.exp_date = self._set_exp_date()
            self.token = self._token_encode()
            self.cookie_manager.set(self.cookie_name, self.token,
                expires_at=datetime.now() + timedelta(days=self.cookie_expiry_days))
            st.session_state['authentication_status'] = True
            return True
        else:
            st.session_state['authentication_status'] = False
            return False

    def create_user(self, form_name: str, location: str = 'main'):
        """
        Creates a register new user widget.

        Parameters
        ----------
        form_name: str
            The rendered name of the register new user form.
        location: str
            The location of the register new user form i.e. main or sidebar.
        Returns
        -------
        bool
            The status of registering the new user, True: user registered successfully.
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == 'main':
            register_user_form = st.form(key="Crear Cuenta")
        elif location == 'sidebar':
            register_user_form = st.sidebar.form('Register user')

        register_user_form.subheader(form_name)
        new_email = register_user_form.text_input('Correo electronico').lower()
        new_username = register_user_form.text_input('Nombre de usuario').lower()
        new_password = register_user_form.text_input('Contraseña', type='password')
        new_password_repeat = register_user_form.text_input('Repita la contraseña', type='password')
        rol = register_user_form.selectbox(
            "Selecciona un Rol",
            ("Editor", "Administrador", "Invitado"),
            index=None,
            placeholder="Rol ...")
        

        if register_user_form.form_submit_button('Registrar'):
        
            #lenght verifications
            if len(new_email)== 0 or len(new_username)== 0 or len(new_password)== 0 : 
                st.warning("Debe completar todos los espacios")
                return False

            if len(new_password) < 6:
                st.warning("La contraseña debe tener una longitud mayor a 6 caracteres")
                return False


            if new_password != new_password_repeat:
                st.warning("La contraseña debe ser la misma")
                return False
            
            if ("@" not in new_email):
                st.warning("Debe ser un correo valido")
                return False
            if db.insert_user(new_username, new_email, self._hash(new_password),rol) == False:
                print("b")
                st.error("Nombre de Usuario no disponible")
                return False
            else:
                st.success("Registrado Correctamente")
                return True

            
    def login(self, form_name: str, location: str = 'main') -> tuple:
        """
        Creates a login widget.

        Parameters
        ----------
        form_name: str
            The rendered name of the login form.
        location: str
            The location of the login form, main or sidebar.
        Returns
        -------
        str
            Name of the authenticated user.
        bool
            The status of authentication, None: no credentials entered, 
            False: incorrect credentials, True: correct credentials.
        str
            Username of the authenticated user.
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if not st.session_state['authentication_status']:
            self._check_cookie()
            if not st.session_state['authentication_status']:
                if location == 'main':
                    login_form = st.form('Login')
                elif location == 'sidebar':
                    login_form = st.sidebar.form('Login')


                login_form.subheader(form_name)
                self.username = login_form.text_input(
                    'Nombre de usuario').lower()
                self.password = login_form.text_input(
                    'Contraseña', type='password')

                if login_form.form_submit_button('Iniciar Sesion'):
                    self._check_credentials()
                                
                st.text("¿No tienes cuenta?")
                create_button=st.button("Crear cuenta")
                if create_button:
                    st.session_state["username"]= "new_user"
                    
        return st.session_state['email'], st.session_state['authentication_status'], st.session_state['username'], st.session_state["role"]
    

    def logout(self, button_name: str, location: str='main', key: str=None):
        """
        Creates a logout button.

        Parameters
        ----------
        button_name: str
            The rendered name of the logout button.
        location: str
            The location of the logout button i.e. main or sidebar.
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == 'main':
            if st.button(button_name, key):
                self.cookie_manager.delete(self.cookie_name)
                st.session_state['logout'] = True
                st.session_state['email'] = None
                st.session_state['username'] = None
                st.session_state['role'] = None
                st.session_state['authentication_status'] = None
        elif location == 'sidebar':
            if st.sidebar.button(button_name, key):
                self.cookie_manager.delete(self.cookie_name)
                st.session_state['logout'] = True
                st.session_state['email'] = None
                st.session_state['username'] = None
                st.session_state['role'] = None
                st.session_state['authentication_status'] = None

    def reset_password(self, username: str, form_name: str, location: str='main'):
        """
        Creates a password reset widget.

        Parameters
        ----------
        username: str
            The username of the user to reset the password for.
        form_name: str
            The rendered name of the password reset form.
        location: str
            The location of the password reset form i.e. main or sidebar.
        Returns
        ---.
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == 'main':
            reset_password_form = st.form('Reset password')
        elif location == 'sidebar':
            reset_password_form = st.sidebar.form('Reset password')
        
        reset_password_form.subheader(form_name)
        current_password = reset_password_form.text_input('Contraseña actual', type='password')
        new_password = reset_password_form.text_input('Nueva contraseña', type='password')
        new_password_repeat = reset_password_form.text_input('Repetir contraseña', type='password')
        if reset_password_form.form_submit_button('Actualizar'):
            if db.check_password(username,current_password ) == False:
                st.error("La contraseña actual es incorrecta")
                return False
            if current_password==0 and new_password == 0 and new_password_repeat==0:
                st.error("Rellene todos los espacios")
                return False
            if current_password == new_password:
                st.warning("La contraseña actual y la nueva son iguales") 
                return False
            if len(new_password) < 6:
                st.warning("La contraseña debe tener una longitud mínima de 6 caracteres")
                return False
            if new_password != new_password_repeat:
                st.error("Debe repetir la misma contraseña")
                return False
            db.update_password(username,self._hash(new_password))
            st.success("Contraseña actualizada")
            return True
            
            
    