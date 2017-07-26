<?PHP //Make sure there are no whitespaces before '<' on this line.
/* vim: set expandtab tabstop=4 shiftwidth=4: */
// +----------------------------------------------------------------------+
// | DB_eSession is a feature packed PHP class that stores session data   |
// | in a MySQL database rather than files. It is powerful, designed with |
// | security in mind, and yet easy to utilize. The code contains lots of |
// | comments, it comes with full documentation, and examples of how to   |
// | use the class including a basic authentication login/logout process. |
// | It includes member functions useful (to webmasters) for monitoring or|
// | viewing, deleting, and altering sessions validity like in the case of|
// | locking one or more sessions upon detection of unauthorized use.     |
// | This custom MySQL database session handler class might just be what  |
// | you're looking to implement on your web or intranet site. Enjoy it!  |
// |                                                                      |
// | This script has been created and released under the GNU GPL and is   |
// | free to use and redistribute only if this whole header comments and  |
// | copyright statement are not removed. Author gives no warranties. Use |
// | at your own risk. Read the copyright, disclaimer, and license.       |
// |                                                                      |
// | System Requirements: Any OS supporting a web server for PHP to run.  |
// | Requires PHP version 4.2.0 or higher, MySQL version 3.22.5 or later. |
// | libmcrypt ver 2.2.x or higher is optional for encryption/decryption. |
// | session.auto_start PHP setting needs to be off. Register_globals can |
// | be on or off.                                                        |
// |                                                                      |
// | Tested under PHP ver 4.3.2/4/5, MySQL version 4.0.15/18, mcrypt 2.4.x|
// |                                                                      |
// +----------------------------------------------------------------------+
// | DB_eSession, Copyright (c) 2004 Lawrence Osiris, All Rights Reserved |
// +----------------------------------------------------------------------+
// | This program is free software; you can redistribute it and/or modify |
// | it under the terms of the GNU General Public License as published by |
// | the Free Software Foundation; either version 2 of the License, or    |
// | (at your option) any later version.                                  |
// |                                                                      |
// | This program is distributed in the hope that it will be useful,      |
// | but WITHOUT ANY WARRANTY; without even the implied warranty of       |
// | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        |
// | GNU General Public License for more details.                         |
// |                                                                      |
// | You should have received a copy of the GNU General Public License    |
// | along with this program; if not, write to the                        |
// |                                                                      |
// | Free Software Foundation, Inc.,                                      |
// | 59 Temple Place, Suite 330,                                          |
// | Boston, MA  02111-1307  USA                                          |
// |                                                                      |
// | Or you may obtain the license at http://www.gnu.org/copyleft/gpl.html|
// |                                                                      |
// +----------------------------------------------------------------------+
// | Author: Lawrence Osiris <code@dearneighbor.com>                      |
// | At web: http://www.code.dearneighbor.com                             |
// |                                                                      |
// | Silas Palmer from Australia, wrote the code in sessEncode and        |
// | sessDecode member functions. Code used with permission and under GNU |
// | GPL too. Web address: http://www.silaspalmer.com                     |
// |                                                                      |
// +----------------------------------------------------------------------+
// |                                                                      |
// |                      C H A N G E   L O G                             |
// |                      -------------------                             |
// |                                                                      |
// | DATE        VERSION  DESCRIPTION                                     |
// | ----------  -------  ----------------------------------------------- |
// | 05/05/2004   1.0.0   Initial code distribution to the general public |
// | 06/03/2004   1.0.1   sessDecode: removed substr() and added trim().  |
// | 08/08/2004   1.0.2   sessDecode: Initialized $_decoded variable.     |
// |                      _getSecID: Commented out HTTP_ACCEPT_ENCODING.  |
// +----------------------------------------------------------------------+


/**
 * DB_ESESSION_LOADED - For checking whether the class has been defined. You can
 * use DB_ESESSION_LOADED or class_exists().
 *
 * @access public
 * @global bool To indicate this class has been loaded (with an include or require)
 */
define('DB_ESESSION_LOADED', TRUE);


/**
 * @package    DB_eSession
 * @license    http://opensource.org/licenses/gpl-license.php GNU Public License
 * @author     Lawrence Osiris <code@dearneighbor.com>
 * @link       http://www.code.dearneighbor.com
 * @copyright  Copyright &copy; 2004, Lawrence Osiris
 * @version    $Version: 1.0.0$
 * @access     public
 */
class DB_eSession
{

    /**
     * @var    string $_ver This scripts version number
     * @access private
     */
    var $_ver = '1.0.0';


    /**
     * @var    string $_REQ_VER The minimum PHP version number this script
     *                          requires in order to execute successfully.
     * @access private
     */
    var $_REQ_VER = '4.2.0';


    /**
     * @var    string $_mysql_ver The current MySQL version number
     * @access private
     */
    var $_mysql_ver = NULL;


    /**
     * @var    int $_dbh The resource link to the session database
     * @access private
     */
    var $_dbh;


    /**
     * @var    array $_db Holds session database access and table info.
     * @access private
     */
    var $_db = array();


    /**
     * @var    array $_sess_opt Holds the session configuration option values
     * @access private
     */
    var $_sess_opt = array();


    /**
     * @var    string $_sess_name Holds the current session name.
     * @access private
     */
    var $_sess_name = NULL;


    /**
     * @var    int $_sess_ID_len Holds the character length of session ID.
     * @access private
     */
    var $_sess_ID_len;


    /**
     * @var    string $_DEFAULT_LANG What the default language code is
     * @access private
     */
    var $_DEFAULT_LANG;


    /**
     * @var    string $_CURRENT_LANG What the current language code in use is
     * @access private
     */
    var $_CURRENT_LANG;


    /**
     * @var    bool   $_stop_on_warn Whether to stop script on encountering a
     *                warning message. Set $_param['stop_on_warn'].
     * @access private
     */
    var $_stop_on_warn;


    /**
     * @var    string $_WRN_COLOR Contains font color for warning messages.
     * @access private
     */
    var $_WRN_COLOR;


    /**
     * @var    string $_WRN_SIZE Contains font size for warning messages.
     * @access private
     */
    var $_WRN_SIZE;


    /**
     * @var    array $_WRN_MSGS Contains warning message constants for ea. lang.
     * @access private
     */
    var $_WRN_MSGS;


    /**
     * @var    string $_warnings Contains any non-fatal warning messages
     * @access private
     */
    var $_warnings = NULL;


    /**
     * @var    bool   $_stop_on_error Whether to stop script on encountering an
     *                error message or not. Set $_param['stop_on_error'].
     * @access private
     */
    var $_stop_on_error;


    /**
     * @var    string $_ERR_COLOR Contains font color for error messages.
     * @access private
     */
    var $_ERR_COLOR;


    /**
     * @var    string $_ERR_SIZE Contains font size for error messages.
     * @access private
     */
    var $_ERR_SIZE;


    /**
     * @var    array $_ERR_MSGS Contains error message constants for ea. lang.
     * @access private
     */
    var $_ERR_MSGS;


    /**
     * @var    string $_errors Contains error messages encountered
     * @access private
     */
    var $_errors = NULL;


    /**
     * @var    bool $_DETAIL_ERR_MSGS Display detail errors/warnings or not.
     * @access private
     */
    var $_DETAIL_ERR_MSGS;


    /**
     * @var    int $_MIN_SESS_ID_LEN Holds the minimum session ID length (12)
     * @access private
     */
    var $_MIN_SESS_ID_LEN = 12;


    /**
     * @var    int $_MAX_SESS_ID_LEN Holds the maximum session ID length of 32
     * @access private
     */
    var $_MAX_SESS_ID_LEN = 32;


    /**
     * @var    int $_SESS_LIFE Holds the session life duration in seconds
     * @access private
     */
    var $_SESS_LIFE;


    /**
     * @var    int $_SESS_TIMEOUT Holds the absolute session life in seconds
     * @access private
     */
    var $_SESS_TIMEOUT;


    /**
     * @var    int $_SEC_LEVEL Holds a number designating session security level
     * @access private
     */
    var $_SEC_LEVEL;

    /**
     * @var    bool $_ENCRYPT A flag to turn on session encryption TRUE/FALSE
     * @access private
     */
    var $_ENCRYPT;


    /**
     * @var    bool $_ENCRYPT_KEY A value used in session encryption/decryption
     * @access private
     */
    var $_ENCRYPT_KEY;

    /**
     * @var    bool $_ENC_KEY_HASHED An md5 value of $_ENCRYPT_KEY for security.
     * @access private
     */
    var $_ENC_KEY_HASHED;


    /**
     * @var    bool $_MCRYPT A flag to indicate if mcrypt library installed
     * @access private
     */
    var $_MCRYPT;


    /**
     * @var    bool $_MCRYPT_LATEST A flag to indicate if it's a newer library
     * @access private
     */
    var $_MCRYPT_LATEST;


    /**
     * @var    string $_KEY_PREFIX A secret key used in prefixing MD5 hashes
     * @access private
     */
    var $_KEY_PREFIX;


    /**
     * @var    string $_KEY_SUFFIX A secret key used in suffixing MD5 hashes
     * @access private
     */
    var $_KEY_SUFFIX;


    /**
     * @var    string $_CONF_PSWD A confirmation password for delete and lock
     * @access private
     */
    var $_CONF_PSWD;


    /**
     * @var    bool $_MAGIC_QUOTES_GPC Determines if GET/POST/COOKIE data are
     *              slashed
     * @access private
     */
    var $_MAGIC_QUOTES_GPC;


    /**
     * @var    bool $_MAGIC_QUOTES_RUNTIME Determines if external source data is
     *              slashed after reads (like from a DB)
     * @access private
     */
    var $_MAGIC_QUOTES_RUNTIME;


    /**
     * @var    bool $_ARG_SEP Output argument separator. Usually '&'.
     * @access private
     */
    var $_ARG_SEP;


    /**
     * @var    bool $_SLASH_ANYWAY Forces addslashes to occur to session data
     * @access private
     */
    var $_SLASH_ANYWAY;


    /**
     * @var    bool $_STRIP_ANYWAY Forces stripslashes to occur to session data
     * @access private
     */
    var $_STRIP_ANYWAY;


    /**
     * @var    bool $_GC_DEL_LOCKED Garbage Collection delete locked session T/F
     * @access private
     */
    var $_GC_DEL_LOCKED;


    /**
     * DB_eSession - Constructor
     * You could change to always pass by reference like this: (&$_param)
     * Or you could leave as is, and pass by reference to save on memory, like
     * this: $sess = new DB_eSession(&$sess_param);
     *
     * @param  array $_param Various database and session setting options
     * @return obj   New instance of DB_eSession class
     * @access private
     */
    function DB_eSession($_param = array())
    {
        define('STOP', TRUE);

        /**
         * Check minimum PHP version number for script to work, and
         * produce error if it doesn't meet that requirement.
         * version_compare() requires PHP v4.1.0 to work but shouldn't
         * use here because current PHP might be less than that.
         */
        if (strcmp($this->_REQ_VER, PHP_VERSION) > 0) {

            $this->_errors = PHP_VERSION . ' < ' . $this->_REQ_VER . "\n";
            /**
             * Display error and stop execution regardless of _stop_on_error
             * setting.
             */
            $this->_handleErrors(STOP);     // Severe error - exit script

        }


        if (is_array($_param)) {
            $_not_array = NULL;

        } else {
            $_not_array = 'NOT_ARRAY';      // For producing a warning
            $_param = array();
        }


        /**
         * Set the default and current language codes for displaying error and
         * warning messages. Default is 'en' for English.
         */
        $this->_DEFAULT_LANG = isSet($_param['default_lang']) ?
                                     $_param['default_lang']  : 'en';


        $this->_CURRENT_LANG = isSet($_param['current_lang']) ?
                                     $_param['current_lang']  :
                                     isSet($_SERVER['HTTP_ACCEPT_LANGUAGE']) ?
                        substr($_SERVER['HTTP_ACCEPT_LANGUAGE'], 0, 2) : 'en';


        /**
         * Set $_param['stop_on_error'] => FALSE to not have this class
         * stop execution upon an error. This means you will handle the
         * error checking and displays in your script. Default is to stop
         * (TRUE). This is used as the initial setting. This can be turned
         * on and off at any time by using stopOnErrors() or endStopOnErrors().
         */
        $this->_stop_on_error = (bool) isSet($_param['stop_on_error']) ?
                                             $_param['stop_on_error']  : TRUE;

        /**
         * Set the font color for error messages (any valid HTML syntax)
         */
        $this->_ERR_COLOR = isSet($_param['error_color']) ?
                                  $_param['error_color']  : 'RED';

        /**
         * Set the font size for error messages (any valid HTML syntax)
         */
        $this->_ERR_SIZE  = isSet($_param['error_size'])  ?
                                  $_param['error_size']   : '+0';

        /**
         * Set $_param['stop_on_warn'] => TRUE to have this class
         * stop execution upon a warning. Default is not to stop (FALSE). This
         * is used as the initial setting. This can be turned on and off at any
         * time by using stopOnWarnings() or endStopOnWarnings().
         */
        $this->_stop_on_warn = (bool) isSet($_param['stop_on_warn']) ?
                                            $_param['stop_on_warn']  : FALSE;

        /**
         * Set the font color for warning messages (any valid HTML syntax)
         */
        $this->_WRN_COLOR = isSet($_param['warn_color']) ?
                                  $_param['warn_color']  : 'BLUE';

        /**
         * Set the font size for warning messages (any valid HTML syntax)
         */
        $this->_WRN_SIZE  = isSet($_param['warn_size'])  ?
                                  $_param['warn_size']   : '+0';

        /**
         * Set to TRUE to display SQL syntax and other values when displaying
         * errors or warning messages encountered. Default is FALSE for security
         * purposes. Turn on mostly when in development or testing your site,
         * but remember to turn it off for a production ready site.
         */
        $this->_DETAIL_ERR_MSGS = (bool) isSet($_param['detail_err_msgs']) ?
                                               $_param['detail_err_msgs']  :
                                               FALSE;


        /**
         * Set $_param['buffer'] => TRUE to have this class
         * execute the ob_start() command to start buffering the output.
         * You may want to use if you can't resolve the 'headers already sent'
         * warning message generated by PHP/this script. The ob_end_flush()
         * is called implicitly at the end of your script. It flushes out the
         * contents of the buffer to the browser, and destroys the current
         * output buffer.
         */
        $_buffer = (bool) isSet($_param['buffer']) ? $_param['buffer'] : FALSE;
        if ($_buffer)
            ob_start();


        /**
         * Set the path and filename of the file containing the errors array
         * constants. You can use relative (recommended) or absolute file paths.
         * For security, specify a filename without the '.php' because the
         * class will automatically add '.php' to the end. i.e. If you specify
         * 'errors.php' this class will try to locate a file called
         * 'errors.php.php'. So, just specify 'errors'. The default path is
         * the current directory (where your script is running from), but
         * but recommend to put the errors file off the web directory along
         * with this class.DB_eSession.php file.
         */
        $_errors_path = isSet($_param['errors_path']) ?
                              $_param['errors_path']  : './';


        $_errors_file = isSet($_param['errors_file']) ?
                              $_param['errors_file']  : 'errors.DB_eSession';

        $_filename = $_errors_path . $_errors_file . '.php';

        if (($this->pregMatches('/^[a-z0-9_.]+$/i', $_errors_file)) &&
            (file_exists($_filename))) {

            $_loaded = require_once($_filename);

        } else {

            $this->_errors = "xxxx --> " . $_filename . " <-- xxxx\n";
            $this->_handleErrors(STOP);     // Severe error - exit script
        }

        if ((0 === strcmp($_loaded, 'LOAD_OK')) &&
            (isSet($_ERR))  &&
            (isSet($_WRN))) {

            $this->_ERR_MSGS = $_ERR;
            $this->_WRN_MSGS = $_WRN;
            unset($_ERR, $_WRN);

        } else {

            $this->_errors = '$_ERR $_WRN xxxx --> ' . $_filename .
                              " <-- xxxx\n";
            $this->_handleErrors(STOP);     // Severe error - exit script
        }


        if (!empty($_not_array))
            // Warning: parameter passed to class is not an array
            $this->_setWrnMsg($_not_array);


        /**
         * Whether or not to encrypt/decrypt the WHOLE session data. This will
         * trigger the use of the mcrypt library or sessEncode/sessDecode.
         * This can be set on or off on the fly and it will work accordingly.
         * The default is off since encryption takes extra resources/time.
        */
        $this->_ENCRYPT = (bool) isSet($_param['encrypt']) ?
                                       $_param['encrypt']  : FALSE;

        /**
         * The key used to encrypt/decrypt individual field data or the whole
         * session data. Keep this key a secret (keep off the web directory).
         * Use readable characters and make at least 62 UNIQUE characters long.
         */
        $this->_ENCRYPT_KEY = isSet($_param['encrypt_key']) ?
                                    $_param['encrypt_key']  :
            "z1Mc6KRxAfNwZ0dGjY5qBXhtrPgJO7eCaUmHvQT3yW8nDsI2VkEpiS4blFoLu9";

        /**
         * Determine if libmcrypt is installed and if it's one of the
         * latest versions.
         */
        $this->_MCRYPT        = extension_loaded('mcrypt');
        $this->_MCRYPT_LATEST = FALSE;
        if ($this->_MCRYPT) {

            if (defined('MCRYPT_TRIPLEDES'))      // Only defined in >= 2.4.x
                $this->_MCRYPT_LATEST = TRUE;

            /**
             * The key field used to encrypt/decrypt using the mcrypt library.
             */
            $this->_ENC_KEY_HASHED = md5($this->_ENCRYPT_KEY);

            $this->_ENC_ALGO = isSet($_param['encrypt_cipher']) ?
                                     $_param['encrypt_cipher']  : MCRYPT_GOST;

            $_algo = mcrypt_list_algorithms();
            if (!in_array($this->_ENC_ALGO, $_algo)) {

                // Could not assign the encryption algorithm...
                $this->_setErrMsg('BAD_ALGO', NULL, $this->_ENC_ALGO);
                $this->_handleErrors();
                $this->_ENC_ALGO = NULL;
            }

            $this->_ENC_MODE = isSet($_param['encrypt_mode']) ?
                                     $_param['encrypt_mode']  : MCRYPT_MODE_CFB;

            $_modes = mcrypt_list_modes();
            if (!in_array($this->_ENC_MODE, $_modes)) {

                // Could not assign the encryption mode...
                $this->_setErrMsg('BAD_ENC_MODE', NULL, $this->_ENC_MODE);
                $this->_handleErrors();
                $this->_ENC_MODE = NULL;

            } else
            if (($this->_ENC_MODE != MCRYPT_MODE_ECB) &&
                ($this->_ENC_MODE != MCRYPT_MODE_CBC) &&
                ($this->_ENC_MODE != MCRYPT_MODE_CFB) &&
                ($this->_ENC_MODE != MCRYPT_MODE_OFB)) {

                // Could not assign the encryption mode...Use class supported
                $this->_setErrMsg('BAD_MODE_SUPP', NULL, $this->_ENC_MODE,
                                  'ECB, CBC, CFB, OFB.');
                $this->_handleErrors();
                $this->_ENC_MODE = NULL;
            }

        } else {

            $this->_ENC_KEY_HASHED = NULL;
            $this->_ENC_ALGO       = NULL;
            $this->_ENC_MODE       = NULL;
        }


        /**
         * As of PHP 4.2.0, there is no need to seed the random number
         * generator, however, we'll do it here for portability. This will be
         * needed for use with the encryption/decryption mcrypt routines and
         * generating of a new session ID.
         */
        mt_srand((double)microtime()*1000000);
        srand((double)microtime()*1000000);


        /**
         * See if MD5 hashing keys have been passed, otherwise set defaults.
         */
        $this->_KEY_PREFIX = isSet($_param['key_prefix']) ?
            $_param['key_prefix'] : 'O9R^3mp#i|34';

        $this->_KEY_SUFFIX = isSet($_param['key_suffix']) ?
            $_param['key_suffix'] : '+t97!u0K-2L5';

        /**
         * A password used to pass to the delete all session/lock functions as a
         * way to confirm the intent of modifying all rows in the sessions
         * table.
         */
        $this->_CONF_PSWD   = isSet($_param['confirm_pswd']) ?
            $_param['confirm_pswd'] : '!*CONFIRMED*!';


        /**
         * Database related variables with assigned default values when not set.
         * Assign these necessary fields to allow connection to the database.
         * Remember to give 'sess_user' access privileges to 'db_esessions'.
         * Make sure the password is correct (sess1234 is the default).
         */
        $this->_db['db_host']       =
            isSet($_param['db_host']) ? $_param['db_host'] : 'localhost';

        $this->_db['db_user']       =
            isSet($_param['db_user']) ? $_param['db_user'] : 'sess_user';

        $this->_db['db_pswd']       =
            isSet($_param['db_pswd']) ? $_param['db_pswd'] : 'sess1234';

        $this->_db['db_name']       =
            isSet($_param['db_name']) ? $_param['db_name'] : 'db_esessions';

        $this->_db['db_persistent'] =
            isSet($_param['db_persistent']) ?
                (bool) $_param['db_persistent'] : FALSE;

        $this->_db['db_resource']   =
            isSet($_param['db_resource']) ? $_param['db_resource'] : NULL;

        /**
         * Optionally supply a database resource link. This class will NOT
         * attempt to connect to MySQL and use the link instead.
         */
        if (is_resource($this->_db['db_resource']))
            $this->_dbh = $this->_db['db_resource'];
        else
            $this->_dbh = NULL;


        /**
         * Table related variables with assigned default values when not set.
         * Assign these necessary fields to allow connection to the 'sessions'
         * table. Specify what each column name is defined as in the table.
         */
        $this->_db['tb_name']       =
            isSet($_param['tb_name'])    ? $_param['tb_name']   : 'eSessions';

        $this->_db['tb_id_col']     =
            isSet($_param['tb_id_col'])  ? $_param['tb_id_col'] : 'sess_id';

        $this->_db['tb_sl_col']     =
            isSet($_param['tb_sl_col'])  ? $_param['tb_sl_col'] :
                'sess_sec_level';

        $this->_db['tb_cr_col']     =
            isSet($_param['tb_cr_col'])  ? $_param['tb_cr_col'] :
                'sess_created';

        $this->_db['tb_ex_col']     =
            isSet($_param['tb_ex_col'])  ? $_param['tb_ex_col'] : 'sess_expiry';

        $this->_db['tb_to_col']     =
            isSet($_param['tb_to_col'])  ? $_param['tb_to_col'] :
                'sess_timeout';

        $this->_db['tb_lk_col']     =
            isSet($_param['tb_lk_col'])  ? $_param['tb_lk_col'] : 'sess_locked';

        $this->_db['tb_vl_col']     =
            isSet($_param['tb_vl_col'])  ? $_param['tb_vl_col'] : 'sess_value';

        $this->_db['tb_iv_col']     =
            isSet($_param['tb_iv_col'])  ? $_param['tb_iv_col'] : 'sess_enc_iv';

        $this->_db['tb_si_col']     =
            isSet($_param['tb_si_col'])  ? $_param['tb_si_col'] : 'sess_sec_id';

        $this->_db['tb_tr_col']     =
            isSet($_param['tb_tr_col'])  ? $_param['tb_tr_col'] : 'sess_trace';


        /**
         * Set $_param['sess_id_len'] to be the length of the session ID.
         * Default of $this->_MAX_SESS_ID_LEN will be used.
         */
        $this->_sess_ID_len         = (int)
            isSet($_param['sess_id_len']) ? intval($_param['sess_id_len']) :
                                            $this->_MAX_SESS_ID_LEN;

        if ($this->_sess_ID_len < $this->_MIN_SESS_ID_LEN)
            $this->_sess_ID_len = $this->_MIN_SESS_ID_LEN;
        else
            if ($this->_sess_ID_len > $this->_MAX_SESS_ID_LEN)
                $this->_sess_ID_len = $this->_MAX_SESS_ID_LEN;

        /**
         * Set $_param['new_sid'] => TRUE to create a new session ID.
         * Default is FALSE. Takes effect before a session_start().
         * This can be set TRUE without setting $_param['sess_id'], in
         * which case, a session ID will be automatically generated.
         */
        $_new_sess_ID               = (bool)
            isSet($_param['new_sid']) ? $_param['new_sid'] : FALSE;

        /**
         * If desired, set $_param['sess_id'] to a valid custom session ID.
         * Works in conjunction with $_param['new_sid'] (must be set to TRUE).
         */
        $_sess_ID                   =
            isSet($_param['sess_id']) ? $_param['sess_id'] : NULL;

        if (!empty($_sess_ID)) {
            if (strlen($_sess_ID) != $this->_sess_ID_len) {

                // Warning: Custom session ID passed is not the right length
                $this->_setWrnMsg('SESS_LENGTH', NULL, $this->_sess_ID_len,
                                  $_param['sess_id']);

                $_sess_ID = NULL;

            } else
                if (!$this->pregMatches('/^[a-zA-Z0-9]+/', $_sess_ID)) {

                    // Warning: Custom session ID passed is invalid.
                    $this->_setWrnMsg('SESS_INVALID', NULL, $_param['sess_id']);

                    $_sess_ID = NULL;
                }
        }


        /**
         * Set $_param['ie_fix'] => TRUE (default) to send a header output to
         * fix the IE bug. See further comments below.
         */
        $_IE_fix                    = (bool)
            isSet($_param['ie_fix'])  ? $_param['ie_fix']  : TRUE;


        /**
         * When set to TRUE, locked session rows will be deleted right
         * away, regardless of their current expiry or timeout settings when
         * the Garbage Collection cleanup/delete function is invoked.
         */
        $this->_GC_DEL_LOCKED = (bool)
            isSet($_param['gc_del_locked']) ? $_param['gc_del_locked'] : FALSE;


        /**
         * Session Runtime Configurations. See:
         * http://us2.php.net/manual/en/ref.session.php
         *
         * Not all can be set or take effect outside of the php.ini
         * configuration file. Some options can be set at runtime without
         * an error produced, but have no effect. i.e. session.auto_start
         *
         * All session options are used here in case there is future support
         * to make option take effect at runtime. i.e. session.use_trans_sid
         *
         * When $_param['stop_on_warn'] is FALSE, check for warning messages
         * using warningsExist().
         */
        $this->_sess_opt['save_path'] =
            isSet($_param['save_path']) ? $_param['save_path'] : 'db_esessions';

        if (isSet($_param['name'])) {
            // Check to make sure name is only alphanumeric
            if (!$this->pregMatches('/^[a-zA-Z0-9]+/', $_param['name'])) {

                // Warning: Session configuration option session.name alpha
                $this->_setWrnMsg('NAME_INVALID', NULL, $_param['name']);

                $this->_sess_opt['name'] = 'eSESSION';

            } else {
                $this->_sess_opt['name'] = $_param['name'];
            }

        } else {

            $this->_sess_opt['name'] = 'eSESSION';
        }

        $this->_sess_opt['save_handler'] =
            isSet($_param['save_handler']) ? $_param['save_handler'] : 'user';

        if (isSet($_param['auto_start']))
            $this->_sess_opt['auto_start'] = (bool) $_param['auto_start'];

        if (isSet($_param['gc_probability']))
            $this->_sess_opt['gc_probability'] = (int)
                (0 == intval($_param['gc_probability'])) ?
                    10 : intval($_param['gc_probability']);

        if (isSet($_param['gc_divisor']))
            $this->_sess_opt['gc_divisor'] = (int)
                (0 == intval($_param['gc_divisor'])) ?
                    100 : intval($_param['gc_divisor']);

        /**
         * There maybe a bug with sessions lifetime under Windows and FAT32 in
         * PHP version 4.1.0/1/2. See: http://bugs.php.net/bug.php?id=14798
         */
        if (isSet($_param['gc_maxlifetime']))
            $this->_sess_opt['gc_maxlifetime'] =
               intval($_param['gc_maxlifetime']);

        if (isSet($_param['serialize_handler']))
            $this->_sess_opt['serialize_handler'] =
                $_param['serialize_handler'];

        if (isSet($_param['cookie_lifetime']))
            $this->_sess_opt['cookie_lifetime'] =
               intval($_param['cookie_lifetime']);

        if (isSet($_param['cookie_path']))
            $this->_sess_opt['cookie_path']   = $_param['cookie_path'];

        if (isSet($_param['cookie_domain']))
            $this->_sess_opt['cookie_domain'] = $_param['cookie_domain'];

        if (isSet($_param['cookie_secure'])) {
            $this->_sess_opt['cookie_secure'] = $_param['cookie_secure'];

            if ((0 === strcmp($this->_sess_opt['cookie_secure'], '1')) &&
                (!$this->secureConnection())) {

                // Warning: You are setting session.cookie_secure - not secure
                $this->_setWrnMsg('NOT_SECURE');

            }

        }

        if (isSet($_param['use_cookies']))
            $this->_sess_opt['use_cookies'] = (bool) $_param['use_cookies'];

        if ((isSet($_param['use_only_cookies'])) &&
            (version_compare(PHP_VERSION, '4.3.0', '>=')))
            $this->_sess_opt['use_only_cookies'] =
               (bool) $_param['use_only_cookies'];

        if (isSet($_param['referer_check']))
            $this->_sess_opt['referer_check'] = $_param['referer_check'];

        if (isSet($_param['entropy_file']))
            $this->_sess_opt['entropy_file'] = $_param['entropy_file'];

        if (isSet($_param['entropy_length']))
            $this->_sess_opt['entropy_length'] =
               intval($_param['entropy_length']);

        if (isSet($_param['cache_limiter']))
            $this->_sess_opt['cache_limiter'] = $_param['cache_limiter'];

        if (isSet($_param['cache_expire']))     // For PHP version >= 4.2.0
            $this->_sess_opt['cache_expire'] = intval($_param['cache_expire']);

        if (isSet($_param['bug_compat_42']))
            $this->_sess_opt['bug_compat_42'] = (bool) $_param['bug_compat_42'];

        if (isSet($_param['bug_compat_warn']))
            $this->_sess_opt['bug_compat_warn'] = (bool)
                $_param['bug_compat_warn'];

        if (version_compare(PHP_VERSION, '5.0.0', '>=')) {

           // session.use_trans_sid can be changed in a script from v5.0.0 on
           if (isSet($_param['use_trans_sid']))
               $this->_sess_opt['use_trans_sid'] = $_param['use_trans_sid'];

           if (isSet($_param['hash_function']))
               $this->_sess_opt['hash_function'] = $_param['hash_function'];

           if (isSet($_param['hash_bits_per_character']))
               $this->_sess_opt['hash_bits_per_character'] =
                   $_param['hash_bits_per_character'];
        }


        /**
         * Set session configuration options. Values will remain during the
         * script's execution, and will be restored at the script's ending.
         */
        foreach ($this->_sess_opt as $_key => $_value) {

            if (FALSE === $this->_setSessOption($_key, $_value))
                // Warning: Session configuration option ... not assigned
                $this->_setWrnMsg('SESS_OPTION', NULL, $_key, $_value);

        }

        /**
         * Support for url_rewriter.tags option since it relates to sessions.
         * Example: Like you might want to add the iframe=src to it, as in:
         * a=href,area=href,frame=src,iframe=src,form=,fieldset=,input=src
         */
        if (isSet($_param['tags'])) {
            if (FALSE === $this->_setSessOption('url_rewriter.tags',
                                                $_param['tags'],
                                                FALSE))
                // Warning: Configuration option [url_rewriter.tags] not assign
                $this->_setWrnMsg('URL_TAGS', NULL, $_param['tags']);

        }


        /**
         * Security Level: A numerical method to represent access authority for
         * current session/web page. The lower the number means the higher the
         * security clearance. In other words, security level 5 can only access
         * all level 5 or higher session/web pages, and nothing lower than 5.
         * Range 0-255. The default is 128. For administration or sensitive pages
         * use 0 (zero) or 1 (one) as a value. A security level can't be changed
         * after a session has been created. So, the first time the session
         * is created with a set security level, it dictates the access
         * authority for the rest of that active session.
         */
        $this->_SEC_LEVEL = isSet($_param['security_level']) ?
                                intval($_param['security_level']) : 128;


        /**
         * Get current setting of sessions life duration in seconds.
         * This is the number of seconds that is allowed to pass since
         * the last time the session data was accessed.
         * Otherwise, default it to 1440 seconds (24 minutes).
         */
        $this->_SESS_LIFE = intval(ini_get('session.gc_maxlifetime'));
        $this->_SESS_LIFE = (int) ($this->_SESS_LIFE < 1) ?
                                   1440 : $this->_SESS_LIFE;

        /**
         * Calculates maximum life of session in seconds. It's three times
         * the length of gc_maxlifetime (for the default). For example: if
         * gc_maxlifetime is 1440 seconds (24 minutes), then session
         * timeout maximum is set to 4320 seconds (72 minutes). The timeout
         * value can't be less than the gc_maxlifetime value.
         */
        if (isSet($_param['timeout'])) {
            $this->_SESS_TIMEOUT = (int)
                (intval($_param['timeout']) < $this->_SESS_LIFE) ?
                    $this->_SESS_LIFE * 3 : intval($_param['timeout']);
        } else {
            $this->_SESS_TIMEOUT = (int) $this->_SESS_LIFE * 3;
        }


        /**
         * Must not send any HTML output before session_start() is invoked.
         * Set a warning message if HTML headers have been sent to the browser.
         * Exception: ob_start() for buffering.
         */
        if (!$_buffer) {
            if (version_compare(PHP_VERSION, '4.3.0', '>=')) {
                $_filename = '';
                $_linenbr  = (int) 0;
                if (headers_sent($_filename, $_linenbr)) {
                    // Warning: HTTP headers already sent - with detail
                    $this->_setWrnMsg('HEADER_SENT_1', NULL, $_filename,
                                      $_linenbr);
                }

            } else
            if (headers_sent()) {
                // Warning: HTTP headers have already been sent - no detail
                $this->_setWrnMsg('HEADER_SENT_2');
            }
        }


        /**
         * Assign session storage tasks to methods in this class.
         */
        if (!session_set_save_handler(array(&$this, '_sessDBOpen'),
                                      array(&$this, '_sessDBClose'),
                                      array(&$this, '_sessDBRead'),
                                      array(&$this, '_sessDBWrite'),
                                      array(&$this, '_sessDBDestroy'),
                                      array(&$this, '_sessDBGC')
                                     )) {

            // execution of session_set_save_handler() failed
            $this->_setErrMsg('HANDLER_FAIL');
            $this->_handleErrors(STOP);     // Severe error - exit script

        }

        $this->_sess_name = session_name();


        /**
         * Set whether the magic quotes GPC that effects slashing quotes of
         * GET/POST/COOKIE data is set.
         */
        $this->_MAGIC_QUOTES_GPC = (bool) get_magic_quotes_gpc();


        /**
         * Set whether the magic quotes runtime that effects slashing quotes of
         * external data sources is set.
         */
        $this->_MAGIC_QUOTES_RUNTIME = (bool) get_magic_quotes_runtime();


        $this->_ARG_SEP = ('' == ini_get('arg_separator.output')) ? '&' :
                                 ini_get('arg_separator.output');


        /**
         * Set TRUE to force addslashes() to occur on session data regardless
         * of the magic quotes runtime option setting. Default is on (TRUE).
         * If you find that data has slashes incorrectly, then turn this off.
         */
        $this->_SLASH_ANYWAY = (bool) isSet($_param['slash_anyway']) ?
                                            $_param['slash_anyway']  : TRUE;

        /**
         * Set TRUE to force stripslashes() to occur on encrypted session data
         * regardless of the magic quotes runtime option setting. The default
         * is on (TRUE). If you find that data is saved incorrectly, then
         * turn this off.
         */
        $this->_STRIP_ANYWAY = (bool) isSet($_param['strip_anyway']) ?
                                            $_param['strip_anyway']  : TRUE;


        /**
         * Try and save the current session ID if one is defined already.
         */
        if (isSet($_COOKIE[$this->_sess_name]))
            $_sess_id_set = $_COOKIE[$this->_sess_name];
        else
        if (isSet($GLOBALS[$this->_sess_name]))
            $_sess_id_set = $GLOBALS[$this->_sess_name];
        else
            $_sess_id_set = NULL;


        /**
         * Create a new session ID when requested, or when the session ID length
         * is less than the standard maximum if a session hasn't been started
         * or created already ($_COOKIE or $GLOBALS[$this->_sess_name]).
         */
        if (($_new_sess_ID) ||
            (($this->_sess_ID_len < $this->_MAX_SESS_ID_LEN) &&
             (!isSet($_COOKIE[$this->_sess_name])) &&
             (!isSet($GLOBALS[$this->_sess_name])))) {
            $this->_setNewSessID($_sess_ID);
        }


        /**
         * When warning flag is set and there's warning messages, stop
         * execution here. No point in proceeding.
         */
        $this->_handleErrors();


        /**
         * By default this class will do a session_start(), however, you may
         * want to turn it off when using the maintenance type of functions.
         */
        $_do_sess_start = (bool) isSet($_param['session_start']) ?
                                       $_param['session_start']  : TRUE;

        /**
         * When session start is requested and $_SESSION doesn't exist, it
         * means that the auto start option is not on, and no session_start()
         * has been invoked yet. So, start a session. This is safer than
         * checking the 'session.auto_start' configuration setting with
         * ini_get(). Otherwise, just make a manual connection to the DB for
         * now (to make the maintenance type of member functions available for
         * use). You would then have to invoke the session_start() from within
        * your script (if desired). If the session is started in your script,
         * then another call to _sessDBOpen will be invoked but it will be
         * handled alright.
         */
        if (($_do_sess_start) &&
            (!isSet($_SESSION)))
            session_start();
        else
        if (!$_do_sess_start)
            $this->_sessDBOpen($this->_sess_opt['save_path'], $this->_sess_name);


        /**
         * If there was a previous session ID set and we now have a new one,
         * then delete the old session row right away without waiting for it to
         * expire first (for security reasons).
         */
        if (($_do_sess_start) &&
            (!empty($_sess_id_set))) {
            if (0 !== strcmp($_sess_id_set, session_id()))
                $this->deleteSession($_sess_id_set);
        }


        /**
         * There is a form bug in IE v6 while using PHP sessions which causes
         * the loss of filled-in information when returning to the form, after
         * already leaving the form page (by any means). A work around is to use
         * the HTTP 1.1 header "Cache-Control: private"
         */
        if ($_IE_fix)
            $this->sendCacheHeader('private');

    }   // End of DB_eSession Constructor



    /**
     * _formatFont - Formats the HTML font color and size attributes to the
     * text that's passed to it.
     *
     * @param  string $_text Text or the data to be enclosed in the font attr.
     * @param  string $_color The font color to use (any valid HTML syntax).
     * @param  string $_size The font size to use (any valid HTML syntax).
     * @return string Returns the text with the font and size attributes added.
     * @access private
     */
    function _formatFont($_text, $_color = 'BLACK', $_size = '+0')
    {
        if (empty($_color))
            $_color = 'BLACK';

        if (empty($_size))
            $_size  = '+0';

        return '<FONT COLOR="' . $_color . '"'  .
                     ' SIZE="' . $_size  . '">' .
                        $_text . '</FONT>';
    }


    /**
     * _setErrMsg - Sets an error message. Fills-in any passed values in order
     * to produce a formatted error message.
     *
     * @param  string $_errMsgKey Name of key to match against array of errors.
     * @param  string $_SQL The value of the last executed SQL command (if any).
     * @param  mixed  Pass one to many arguments to use as fill-in values for
     *                the error messages.
     * @return bool   Returns TRUE when error message set, or FALSE on failure.
     * @access private
     */
    function _setErrMsg ($_errMsgKey = '', $_SQL = NULL)
    {

        $_lang = $this->_CURRENT_LANG;

        if (!isSet($this->_ERR_MSGS[$_errMsgKey][$_lang])) {

            if (isSet($this->_ERR_MSGS[$_errMsgKey][$this->_DEFAULT_LANG])) {
                // Error message not found in current lang; switching to def.
                $_lang = $this->_DEFAULT_LANG;
            } else {
                // Could not find the supplied key of error message
                $this->_errors .= '$_ERR[\'' . $_errMsgKey . "']\n";
                return FALSE;
            }
        }

        if (@func_num_args() > 2) {     // Do we have extra argument values?

            $_arg = @func_get_args();

            array_shift($_arg);         // Remove $_errMsgKey value passed
            array_shift($_arg);         // Remove $_SQL value passed

            $_cnt = count($_arg);

            /**
             * Create a pattern for the number of arguments passed
             */
            $_patterns = str_repeat('/%s/i,', $_cnt);
            $_patterns = explode(',', $_patterns);
            array_pop($_patterns);      // Remove extra entry created by explode

            /**
             * When no detail requested, replace argument values with [xxx]
             */
            for ($i = 0; $i < $_cnt; $i++) {
                if ($this->_DETAIL_ERR_MSGS)
                    // Slash $ signs that's in the data for displaying correctly
                    $_arg[$i] = str_replace('$', '\$', $_arg[$i]);
                else
                    $_arg[$i] = '[xxx]';

            }

            /**
             * Replace the '%s' place holder with argument values passed
             * sprintf() doesn't allow array arguments.
             */
            $_err = @preg_replace($_patterns,
                                  $_arg,
                                  $this->_ERR_MSGS[$_errMsgKey][$_lang],
                                  1
                                 );

        } else {    // No extra arguments were passed

            $_err = $this->_ERR_MSGS[$_errMsgKey][$_lang];
        }

        if (!empty($_SQL)) {

            switch ($this->_DETAIL_ERR_MSGS) {

                case TRUE:

                    $_err .= "SQL: $_SQL\nErr # " .
                             @mysql_errno($this->_dbh) . ': '  .
                             @mysql_error($this->_dbh) . "\n";

                    break;

                default:

                    $_err .= "SQL Err # " .
                             @mysql_errno($this->_dbh) . ': '  .
                             @mysql_error($this->_dbh) . "\n";
            }

        }

        $this->_errors .= $_err;

        return TRUE;
    }


    /**
     * _setWrnMsg - Sets a warning message. Fills-in any passed values in order
     * to produce a formatted warning message.
     *
     * @param  string $_wrnMsgKey Name of key to match against array of warnings
     * @param  string $_SQL The value of the last executed SQL command (if any).
     * @param  mixed  Pass one to many arguments to use as fill-in values for
     *                the warning messages.
     * @return bool   Returns TRUE when warning message set, or FALSE on failure
     * @access private
     */
    function _setWrnMsg ($_wrnMsgKey = '', $_SQL = NULL)
    {

        $_lang = $this->_CURRENT_LANG;

        if (!isSet($this->_WRN_MSGS[$_wrnMsgKey][$_lang])) {

            if (isSet($this->_WRN_MSGS[$_wrnMsgKey][$this->_DEFAULT_LANG])) {
                // Warning message not found in current lang; switching to def.
                $_lang = $this->_DEFAULT_LANG;
            } else {
                // Could not find the supplied key of warning message
                $this->_warnings .= '$_WRN[\'' . $_wrnMsgKey . "']\n";
                return FALSE;
            }
        }

        if (@func_num_args() > 2) {     // Do we have extra argument values?

            $_arg = @func_get_args();

            array_shift($_arg);         // Remove $_wrnMsgKey value passed
            array_shift($_arg);         // Remove $_SQL value passed

            $_cnt = count($_arg);

            /**
             * Create a pattern for the number of arguments passed
             */
            $_patterns = str_repeat('/%s/i,', $_cnt);
            $_patterns = explode(',', $_patterns);
            array_pop($_patterns);      // Remove extra entry created by explode

            /**
             * When no detail requested, replace argument values with [xxx]
             */
            for ($i = 0; $i < $_cnt; $i++) {
                if ($this->_DETAIL_ERR_MSGS)
                    // Slash $ signs that's in the data for displaying correctly
                    $_arg[$i] = str_replace('$', '\$', $_arg[$i]);
                else
                    $_arg[$i] = '[xxx]';

            }

            /**
             * Replace the '%s' place holder with argument values passed
             * sprintf() doesn't allow array arguments.
             */
            $_wrn = @preg_replace($_patterns,
                                  $_arg,
                                  $this->_WRN_MSGS[$_wrnMsgKey][$_lang],
                                  1
                                 );

        } else {    // No extra arguments were passed

            $_wrn = $this->_WRN_MSGS[$_wrnMsgKey][$_lang];
        }

        if (!empty($_SQL)) {

            switch ($this->_DETAIL_ERR_MSGS) {

                case TRUE:

                    $_wrn .= "SQL: $_SQL\nErr # " .
                             @mysql_errno($this->_dbh) . ': '  .
                             @mysql_error($this->_dbh) . "\n";

                    break;

                default:

                    $_wrn .= "SQL Err # " .
                             @mysql_errno($this->_dbh) . ': '  .
                             @mysql_error($this->_dbh) . "\n";
            }

        }

        $this->_warnings .= $_wrn;

        return TRUE;
    }


    /**
     * _handleErrors - Detects if errors have occurred and ends the script when
     * the flag is set to stop. Errors are always displayed before warnings.
     *
     * @param  bool   $_stop Flags whether to stop script anyway (on severe
     *                errors.
     * @return bool   Always returns TRUE.
     * @access private
     */
    function _handleErrors($_stop = FALSE)
    {

        if (($this->warningsExist()) &&
            ($this->_stop_on_warn))  {

             if ($this->errorsExist())
                 echo $this->getErrors($this->_ERR_COLOR, $this->_ERR_SIZE);

             echo $this->getWarnings($this->_WRN_COLOR, $this->_WRN_SIZE);

            exit;
        }

        if (($this->errorsExist()) &&
            ($this->_stop_on_error)) {

            echo $this->getErrors($this->_ERR_COLOR, $this->_ERR_SIZE);

            if ($this->warningsExist())
                echo $this->getWarnings($this->_WRN_COLOR, $this->_WRN_SIZE);

            exit;
        }

        if (!is_bool($_stop))
            $_stop = FALSE;

        if ($_stop) {

            if ($this->errorsExist())
                echo $this->getErrors($this->_ERR_COLOR, $this->_ERR_SIZE);

            if ($this->warningsExist())
                echo $this->getWarnings($this->_WRN_COLOR, $this->_WRN_SIZE);

            exit;
        }

        return TRUE;
    }


    /**
     * _setSessOption - Sets the value of the given session configuration option
     *
     * @param  string $_config_option Session related configuration option
     * @param  mixed  $_value The value to assign the configuration option
     * @param  bool   $_check_sess Flags whether to verify 'session.' exists
     * @return mixed  Returns the old value on success, FALSE on failure.
     * @access private
     */
    function _setSessOption($_config_option, $_value, $_check_sess = TRUE)
    {

        $_config_option = trim($_config_option);

        if (empty($_config_option)) {

            return FALSE;

        } else {

            // When TRUE, check to see if 'session.' is included
            if ($_check_sess) {
                // Add 'session.' if not included in $_config_option
                if (0 !== strpos(strtolower($_config_option), 'session.'))
                    $_config_option = 'session.' . $_config_option;

            }

            return ini_set($_config_option, $_value);

        }
    }


    /**
     * _genString - Generates random characters from 1 to 32 in length.
     * 32 characters is the default when length not specified.
     *
     * @param  int    $_length The number of characters to generate.
     * @return string Returns a string of the requested number of characters.
     * @access private
     */
    function _genString($_length = 0)
    {

        $_length = intval($_length);

        if (($_length < 1) ||
            ($_length > $this->_MAX_SESS_ID_LEN))
             $_length = $this->_MAX_SESS_ID_LEN;

        /**
         * Random number seeding already performed in constructor.
         */
        $_string = md5(uniqid(mt_rand(), TRUE));

        return substr($_string, 0, $_length);

    }


    /**
     * _setNewSessID - Creates and sets a new session ID.
     * This is called before session_start() and before any output to the
     * browser.
     *
     *   Note: It's possible if you have PHP version 4.3.2 or higher and are
     *         using the default maximum session length (32), to call
     *         this member function, without an argument, & no output sent
     *         to the browser, after a session_start() has been executed.
     *         That will invoke session_regenerate_id(), which seems to work
     *         correctly (member could have been made public for that reason).
     *         If session_start() has been executed already, then doing
     *         session_id('somevalue') will NOT change the session ID properly.
     *         It's less problematic to keep as a private method (and call
     *         before a session_start()).
     *
     * @param  string $_sess_id An optional session ID to use (of _sess_ID_len)
     * @return string Returns the new session ID.
     * @access private
     */
    function _setNewSessID($_sess_id = NULL)
    {

        global $HTTP_GET_VARS, $HTTP_POST_VARS, $HTTP_COOKIE_VARS;

        $_continue = TRUE;

        /**
         * If supplied with a session ID, validate it and use it when it's good.
         */
        if (strlen($_sess_id) == $this->_sess_ID_len) {
            if (!$this->pregMatches('/^[a-zA-Z0-9]+/', $_sess_id)) {
                // Warning: Custom session ID passed is invalid.
                $this->_setWrnMsg('SESS_INVALID', NULL, $_sess_id);

                $this->_handleErrors();

                // Ignoring value and assigning a new session ID.
                $this->_setWrnMsg('NEW_SESS_ID');

            } else {

                session_id($_sess_id);

                $_continue = FALSE;

            }

        }


        /**
         * Use session_regenerate_id() when the session ID length desired is the
         * same as the maximum allowed, because it generates the maximum length.
         * It is only available in PHP version 4.3.2 or higher. As of PHP 4.3.3,
         * if session cookies are enabled, use of session_regenerate_id() is
         * supposed to submit a new session cookie with the new session id.
         */
        if (($_continue) &&
            ($this->_sess_ID_len == $this->_MAX_SESS_ID_LEN) &&
            (version_compare(PHP_VERSION, '4.3.2', '>='))) {
            if (session_regenerate_id()) {

                $_sess_id  = session_id();

                $_continue = FALSE;

            }

        }


        if ($_continue) {

            $_sess_id = $this->_genString($this->_sess_ID_len);

            session_id($_sess_id);
        }

        // To be safe set...
        if (isSet($_REQUEST[$this->_sess_name]))
            $_REQUEST[$this->_sess_name] = $_sess_id;

        if (isSet($_GET[$this->_sess_name]))
            $_GET[$this->_sess_name] = $_sess_id;

        if (isSet($HTTP_GET_VARS[$this->_sess_name]))
            $HTTP_GET_VARS[$this->_sess_name] = $_sess_id;

        if (isSet($_POST[$this->_sess_name]))
            $_POST[$this->_sess_name] = $_sess_id;

        if (isSet($HTTP_POST_VARS[$this->_sess_name]))
            $HTTP_POST_VARS[$this->_sess_name] = $_sess_id;

        if (isSet($_COOKIE[$this->_sess_name]))
            $_COOKIE[$this->_sess_name]  = $_sess_id;

        // May not actually change until next refresh
        if (isSet($HTTP_COOKIE_VARS[$this->_sess_name]))
            $HTTP_COOKIE_VARS[$this->_sess_name] = $_sess_id;

        if (isSet($GLOBALS[$this->_sess_name]))
            $GLOBALS[$this->_sess_name] = $_sess_id;

        return $_sess_id;
    }


    /**
     * _getSecID - Creates an MD5 of a users trace information. Used to verify
     * session belongs to same user. Not full-proof but adequate.
     * Note: Not using HTTP_ACCEPT since results are inconsistent in IE6.
     *
     * @return string  An MD5 hash of secret keys plus server collected data.
     * @access private
     */
    function _getSecID()
    {

        $_type_used = NULL;
        $_IP = $this->getIPAddr($_type_used);

        $_agent    = isSet($_SERVER['HTTP_USER_AGENT']) ?
                           $_SERVER['HTTP_USER_AGENT']  : 'NO USER AGENT';

/* Rev 1.0.2: Found IE 6 to not return consistent results (under HTTPS)
        $_encoding = isSet($_SERVER['HTTP_ACCEPT_ENCODING']) ?
                           $_SERVER['HTTP_ACCEPT_ENCODING']  : 'NO ENCODING';
*/
        return md5($this->_KEY_PREFIX  .
                   $_IP                .
                   $_type_used         .
                   $_agent             .
//***              $_encoding          .    Rev 1.0.2: Found as unreliable
                   $this->_KEY_SUFFIX
                  );

    }


    /**
     * _getSessTrace - Creates a concatenated string of users trace information.
     * Used for tracing IP in case of unauthorized intruder. Not using secret
     * key here, or in the same order as session security ID. MySQL will
     * truncate at INSERT if character length is longer than column limit.
     * The '~' is used as a delimiter.
     *
     * @return string  A non-hash of server collected data used for tracing.
     * @access private
     */
    function _getSessTrace()
    {

        $_type_used = NULL;
        $_IP = $this->getIPAddr($_type_used);

        $_agent    = isSet($_SERVER['HTTP_USER_AGENT']) ?
                           $_SERVER['HTTP_USER_AGENT']  : 'NO USER AGENT';

        $_accept   = isSet($_SERVER['HTTP_ACCEPT']) ?
                           $_SERVER['HTTP_ACCEPT']  : 'NO ACCEPT';

        $_encoding = isSet($_SERVER['HTTP_ACCEPT_ENCODING']) ?
                           $_SERVER['HTTP_ACCEPT_ENCODING']  : 'NO ENCODING';

        return ($_type_used  . '~' .
                $_IP         . '~' .
                $_agent      . '~' .
                $_accept     . '~' .
                $_encoding
               );

    }


    /**
     * _sessDBOpen - Connects and selects the database.
     *
     * @param  string $_save_path Session save location path.
     * @param  string $_session_name Alphanumeric session name (used in URL's).
     * @return bool   TRUE on good connection and select of DB, FALSE on errors.
     * @access private
     */
    function _sessDBOpen($_save_path, $_session_name)
    {

        // Override _sess_name with what PHP thinks is the session name.
        $this->_sess_name = $_session_name;

        /**
         * When no resource link initially supplied, connect to database.
         */
       if (!is_resource($this->_dbh)) {
            if ($this->_db['db_persistent']) {
                $this->_dbh = @mysql_pconnect($this->_db['db_host'],
                                              $this->_db['db_user'],
                                              $this->_db['db_pswd']
                                             );
            } else {
                $this->_dbh = @mysql_connect ($this->_db['db_host'],
                                              $this->_db['db_user'],
                                              $this->_db['db_pswd']
                                             );
            }
        }

        if (!$this->_dbh)

            // Connection to MySQL server failed
            $this->_setErrMsg('CONNECT_FAIL');     // No error code available
        else {
            $_db_select = @mysql_select_db($this->_db['db_name'], $this->_dbh);

            if (!$_db_select)
                // Could not select MySQL database
                $this->_setErrMsg('SELECTDB_FAIL', 'mysql_select_db',
                                  $this->_db['db_name']);
        }


        $this->_handleErrors();


        if ((!$this->_dbh) ||
            (!$_db_select)) {

            return (bool) FALSE;

        } else {

            $this->_mysql_ver = @mysql_get_server_info($this->_dbh);
            return (bool) TRUE;
        }
    }


    /**
     * _sessDBClose - Closes the connection to the database for non-persistent
     *                connections.
     *
     * @return bool   Always returns TRUE.
     * @access private
     */
    function _sessDBClose()
    {

        if ((!$this->_db['db_persistent']) &&
            (is_resource($this->_dbh)))
            if (!@mysql_close($this->_dbh))
                // Warning: Could not close MySQL database
                $this->_setWrnMsg('CLOSEDB_FAIL', 'mysql_close',
                                  $this->_db['db_name']);

        $this->_handleErrors();

        return (bool) TRUE;
    }


    /**
     * _sessDBRead - Retrieves session data from the table. If encrypted, the
     * data will automatically be decrypted before returning the value back.
     *
     * @param  string $_sess_id Session ID of the row to retrieve.
     * @return string The session data is returned or an empty string on error.
     * @access private
     */
    function _sessDBRead($_sess_id)
    {

        $_time      = time();
        $_sec_level = $this->_SEC_LEVEL;
        $_sec_ID    = $this->_getSecID();

        $_sql  = 'SELECT '    . $this->_db['tb_vl_col']  .
                         ', ' . $this->_db['tb_iv_col']  .
                 '  FROM '  . $this->_db['tb_name']    .
                 ' WHERE (' . $this->_db['tb_id_col']  . " = '$_sess_id')" .
                 '   AND (' . $this->_db['tb_sl_col']  . " <= '$_sec_level')" .
                 '   AND (' . $this->_db['tb_ex_col']  . " > '$_time')" .
                 '   AND (' . $this->_db['tb_to_col']  . " > '$_time')" .
                 '   AND (' . $this->_db['tb_lk_col']  . " = '0')" .
                 '   AND (' . $this->_db['tb_si_col']  . " = '$_sec_ID')";

        $_result = @mysql_query($_sql, $this->_dbh);

        if (!$_result) {

            // Main select/read query failed. Could not read session data
            $this->_setErrMsg('READ_FAILED', $_sql, $_sess_id);

            $this->_handleErrors();

            return (string) ''; // Return empty string on error

        } else {

            $_row = @mysql_fetch_assoc($_result);

            if (!$_row) {

                return (string) ''; // No data found, return an empty string

            } else {

                $_row[$this->_db['tb_vl_col']] =
                    isSet($_row[$this->_db['tb_vl_col']]) ?
                          $_row[$this->_db['tb_vl_col']]  : '';

                $_row[$this->_db['tb_iv_col']] =
                    isSet($_row[$this->_db['tb_iv_col']]) ?
                          $_row[$this->_db['tb_iv_col']]  : '';

                if ($this->_MAGIC_QUOTES_RUNTIME) {
                    $_row[$this->_db['tb_vl_col']] =
                        stripslashes($_row[$this->_db['tb_vl_col']]);

                    $_row[$this->_db['tb_iv_col']] =
                        stripslashes($_row[$this->_db['tb_iv_col']]);
                }

                /**
                 * Decrypt the data if it was encrypted
                 */
                if ((!empty($_row[$this->_db['tb_iv_col']])) &&
                    (!empty($_row[$this->_db['tb_vl_col']]))) {

                    $_row[$this->_db['tb_vl_col']] =
                        $this->sessDecrypt($_row[$this->_db['tb_vl_col']],
                                           $_row[$this->_db['tb_iv_col']],
                                           TRUE);
                }
                                      // When invoked, did decrypt fail?
                return (string) (FALSE === $_row[$this->_db['tb_vl_col']]) ?
                                 '' : $_row[$this->_db['tb_vl_col']];

            }
        }
    }


    /**
     * _sessDBWrite - Inserts or updates session data to the table.
     *
     * @param  string $_sess_id Session ID which is used as the primary key.
     * @param  string $_sess_data Session data to save in the database.
     * @return bool   TRUE on a successful Insert/Update, and FALSE on error.
     * @access private
     */
    function _sessDBWrite($_sess_id, $_sess_data)
    {

        $_time      = time();
        $_expiry    = $_time + $this->_SESS_LIFE;
        $_timeout   = $_time + $this->_SESS_TIMEOUT;
        $_sec_level = $this->_SEC_LEVEL;
        $_sec_ID    = $this->_getSecID();
        $_trace     = addslashes($this->_getSessTrace());
        $_enc_iv    = '';

        /**
         * Encrypt the whole session data when flag is set to TRUE.
         */
        if ($this->_ENCRYPT) {

            /**
             * When magic quotes GPC option is on or strip anyway option
             * is on, strip session data before encrypting. We don't need
             * the slashes when encrypting because the data value will change.
             */
            if (($this->_MAGIC_QUOTES_GPC) ||
                ($this->_STRIP_ANYWAY))
                $_sess_data = stripslashes($_sess_data);

            $_sess_data = $this->sessEncrypt($_sess_data, $_enc_iv, TRUE);
        }

        /**
         * When magic quotes GPC option is off or slash anyway option
         * is on, slash quotes in session data and encryption IV.
         */
        if ((!$this->_MAGIC_QUOTES_GPC) ||
            ($this->_SLASH_ANYWAY)) {

            $_sess_data = addslashes($_sess_data);
            $_enc_iv    = addslashes($_enc_iv);
        }

        $_sql = 'INSERT INTO ' . $this->_db['tb_name']     .
                          ' (' . $this->_db['tb_id_col']   .
                          ', ' . $this->_db['tb_sl_col']   .
                          ', ' . $this->_db['tb_cr_col']   .
                          ', ' . $this->_db['tb_ex_col']   .
                          ', ' . $this->_db['tb_to_col']   .
                          ', ' . $this->_db['tb_lk_col']   .
                          ', ' . $this->_db['tb_vl_col']   .
                          ', ' . $this->_db['tb_iv_col']   .
                          ', ' . $this->_db['tb_si_col']   .
                          ', ' . $this->_db['tb_tr_col']   .
                  ') VALUES (' .
                               "'$_sess_id'"   .
                             ", '$_sec_level'" .
                             ", '$_time'"      .
                             ", '$_expiry'"    .
                             ", '$_timeout'"   .
                             ", '0'"           .
                             ", '$_sess_data'" .
                             ", '$_enc_iv'"    .
                             ", '$_sec_ID'"    .
                             ", '$_trace'"     .
                            ')';

        $_result = @mysql_query($_sql, $this->_dbh);

        if (!$_result) {

            $_errno = @mysql_errno($this->_dbh);

            if ((1062 == $_errno) ||    // ER_DUP_ENTRY
                (1022 == $_errno)) {    // ER_DUP_KEY

                $_sql = 'UPDATE ' . $this->_db['tb_name']     .
                          ' SET '                             .
                                    $this->_db['tb_ex_col']   .
                                    "='$_expiry'"             .
                             ', ' . $this->_db['tb_vl_col']   .
                                    "='$_sess_data'"          .
                             ', ' . $this->_db['tb_iv_col']   .
                                    "='$_enc_iv'"             .
                        ' WHERE ('. $this->_db['tb_id_col']   .
                                    " = '$_sess_id')"         .
                        '   AND ('. $this->_db['tb_cr_col']   .
                                    " < '$_time')"            .
                        '   AND ('. $this->_db['tb_sl_col']   .
                                    " <= '$_sec_level')"      .
                        '   AND ('. $this->_db['tb_ex_col']   .
                                    " > '$_time')"            .
                        '   AND ('. $this->_db['tb_to_col']   .
                                    " > '$_time')"            .
                        '   AND ('. $this->_db['tb_lk_col']   .
                                    " = '0')"                 .
                        '   AND ('. $this->_db['tb_si_col']   .
                                    " = '$_sec_ID')";

                $_result = @mysql_query($_sql, $this->_dbh);

                if (!$_result) {

                    // Update failed. Could not update session data
                    $this->_setErrMsg('UPDATE_FAILED', $_sql, $_sess_id);

                }

            } else {

                // Insert failed. Could not insert session data
                $this->_setErrMsg('INSERT_FAILED', $_sql, $_sess_id);

                if (1064 == $_errno) {  // ER_PARSE_ERROR
                    // Data may contain single quotes without backslashes
                    $this->_setErrMsg('PARSE_ERROR', $_sql);

                    if (($this->_MAGIC_QUOTES_GPC) &&
                        (!$this->_SLASH_ANYWAY)) {

                        // Recommend to turn on param['slash_anyway'] to TRUE
                        $this->_setErrMsg('RECOMD_SLASH');

                    }
                }

            }
        }

        $this->_handleErrors();

        return (bool) $_result;
    }


    /**
     * _sessDBDestroy - Deletes session data from the table. Automatically
     *                  executed when session_destroy() is executed.
     *
     * @param  string  $_sess_id Session ID of the row to delete.
     * @return bool    TRUE on a successful delete, and FALSE on error.
     * @access private
     */
    function _sessDBDestroy($_sess_id)
    {

        global $HTTP_GET_VARS, $HTTP_POST_VARS, $HTTP_COOKIE_VARS;


        $_sql = 'DELETE FROM ' . $this->_db['tb_name'] .
                     ' WHERE ' . $this->_db['tb_id_col']  .
                                 " = '$_sess_id'";

        $_result = @mysql_query($_sql, $this->_dbh);

        if (!$_result) {
            // Destroy failed. Could not delete session data
            $this->_setErrMsg('DESTROY_FAIL', $_sql, $_sess_id);
            $this->_handleErrors();
        }


        session_unset();

        // To be safe remove...
        if (isSet($_REQUEST[$this->_sess_name]))
            unset($_REQUEST[$this->_sess_name]);

        if (isSet($_GET[$this->_sess_name]))
            unset($_GET[$this->_sess_name]);

        if (isSet($HTTP_GET_VARS[$this->_sess_name]))
            unset($HTTP_GET_VARS[$this->_sess_name]);

        if (isSet($_POST[$this->_sess_name]))
            unset($_POST[$this->_sess_name]);

        if (isSet($HTTP_POST_VARS[$this->_sess_name]))
            unset($HTTP_POST_VARS[$this->_sess_name]);

        if (isSet($_COOKIE[$this->_sess_name]))
            unset($_COOKIE[$this->_sess_name]);

        if (isSet($HTTP_COOKIE_VARS[$this->_sess_name]))
            unset($HTTP_COOKIE_VARS[$this->_sess_name]);

        if (isSet($GLOBALS[$this->_sess_name]))
            unset($GLOBALS[$this->_sess_name]);

        return (bool) $_result;
    }


    /**
     * _sessDBGC - Deletes expired session data from the table. It deletes
    *             sessions that expire by inactivity timeout, absolute
     *             timeout, or that are flagged as locked.
     *
     * @param  int    $_maxlifetime Session's life setting in seconds.
     * @return bool   TRUE on successful deletes, and FALSE on error.
     * @access private
     */
    function _sessDBGC($_maxlifetime)
    {

        $_time = time();

        $_sql = 'DELETE FROM ' . $this->_db['tb_name'] .
                     ' WHERE ' .
                               '(' . $this->_db['tb_ex_col'] .
                               " < '" . ($_time - $_maxlifetime) . "')" .
                               ' OR ' .
                               '(' . $this->_db['tb_to_col'] . " < '$_time')";

        if ($this->_GC_DEL_LOCKED) {
            $_sql .=           ' OR ' .
                               '(' . $this->_db['tb_lk_col'] . " = '1')";
        }

        $_result = @mysql_query($_sql, $this->_dbh);

        if (!$_result) {
            // Delete failed during garbage collection/cleanup
            $this->_setErrMsg('GARBAGE_FAIL', $_sql);
            $this->_handleErrors();
        }

        return (bool) $_result;
    }



    /***************************************************************************
     *
     * Start of Public Member Functions
     *
     ***************************************************************************/



    /**
     * getDBResource - Returns the current established MySQL resource link.
     * It can be used in your script to access other tables/databases.
     *
     * @return resource Returns a MySQL resource link identifier.
     * @access public
     */
    function getDBResource()
    {
        return $this->_dbh;
    }


    /**
     * getSessInfo - This will return column information for the session ID
     * passed. The current session ID is used when no session ID is passed.
     * It returns an associative array with the table column names as the key.
     * The session data value, and encryption IV column values are returned
     * only when a confirm password is passed. If the session value is
     * encrypted, it will automatically be decrypted, however the session
     * value data will be raw (in serialized format).
     * The other columns retrieved are useful for determining when a session
     * was created/started and when it will expire.
     * If $_full_exp is FALSE, only the session ID is used to retrieve the row.
     *
     * The trace column can be split into individual values. For example:
     * $fields = $sess->getSessInfo();
     * $arr = explode('~', $fields['sess_trace']); // $arr[1] is IP Address
     *
     * You can use PHP's getdate() function to convert the columns that contain
     * epoch values (such as session created, expiry, and timeout).
     * @link   http://us4.php.net/manual/en/function.getdate.php
     *
     * @param  string $_sess_id The session ID to look for (default is current)
     * @param  bool   $_full_exp Use the full expression in the WHERE clause.
     *                Only used when the session ID is the active one (TRUE def)
     * @param  string $_confirmation_pswd Pass to retrieve raw session value.
     * @return mixed  Returns an assoc. array of data or FALSE on error/no data.
     * @access public
     */
    function getSessInfo($_sess_id = NULL,
                         $_full_exp = TRUE,
                         $_confirmation_pswd = NULL)
    {

        $_sess_id = empty($_sess_id) ? session_id() : $_sess_id;

        /**
         * Verify that raw session value is requested to be retrieved as well
         * by checking the passed password against the confirm password
         * defined in _param['confirm_pswd']
         */
        $_pswd_valid = (0 === strcmp($_confirmation_pswd, $this->_CONF_PSWD)) ?
                        TRUE : FALSE;

        $_sql  = 'SELECT '    . $this->_db['tb_id_col'] .
                         ', ' . $this->_db['tb_sl_col'] .
                         ', ' . $this->_db['tb_cr_col'] .
                         ', ' . $this->_db['tb_ex_col'] .
                         ', ' . $this->_db['tb_to_col'] .
                         ', ' . $this->_db['tb_lk_col'] .
                         ', ' . $this->_db['tb_si_col'] .
                         ', ' . $this->_db['tb_tr_col'];

        if ($_pswd_valid)
            $_sql  .=    ', ' . $this->_db['tb_vl_col'] .
                         ', ' . $this->_db['tb_iv_col'];

        $_sql .= '  FROM '  . $this->_db['tb_name']     .
                 ' WHERE (' . $this->_db['tb_id_col']   . " = '$_sess_id')";

        /**
         * When requested to use full search expressions and the session ID is
         * the same as the current active session ID, use all the rest of the
         * search criteria/fields.
         */
        if (($_full_exp) &&
            (0 === strcmp($_sess_id, session_id()))) {

            $_time      = time();
            $_sec_level = $this->_SEC_LEVEL;
            $_sec_ID    = $this->_getSecID();

            $_sql      .=
                 ' AND (' . $this->_db['tb_sl_col'] . " <= '$_sec_level')" .
                 ' AND (' . $this->_db['tb_ex_col'] . " > '$_time')" .
                 ' AND (' . $this->_db['tb_to_col'] . " > '$_time')" .
                 ' AND (' . $this->_db['tb_lk_col'] . " = '0')" .
                 ' AND (' . $this->_db['tb_si_col'] . " = '$_sec_ID')";

        }

        $_result = @mysql_query($_sql, $this->_dbh);

        if (!$_result) {

            // Session info. query failed. Could not read session data
            $this->_setErrMsg('INFO_FAIL', $_sql, $_sess_id);
            $this->_handleErrors();

            return FALSE;

        } else {

            $_row = @mysql_fetch_assoc($_result);

            if (!$_row) {
                // Warning: No session data found while doing session info query
                $this->_setWrnMsg('NO_SESS_INFO', $_sql, $_sess_id);
                $this->_handleErrors();

            } else
            if ($_pswd_valid) {

                $_row[$this->_db['tb_vl_col']] =
                    isSet($_row[$this->_db['tb_vl_col']]) ?
                          $_row[$this->_db['tb_vl_col']]  : '';

                $_row[$this->_db['tb_iv_col']] =
                    isSet($_row[$this->_db['tb_iv_col']]) ?
                          $_row[$this->_db['tb_iv_col']]  : '';

                if ($this->_MAGIC_QUOTES_RUNTIME) {
                    $_row[$this->_db['tb_vl_col']] =
                        stripslashes($_row[$this->_db['tb_vl_col']]);

                    $_row[$this->_db['tb_iv_col']] =
                        stripslashes($_row[$this->_db['tb_iv_col']]);
                }

                /**
                 * Decrypt the data if it was encrypted
                 */
                if ((!empty($_row[$this->_db['tb_iv_col']])) &&
                   (!empty($_row[$this->_db['tb_vl_col']]))) {

                    $_row[$this->_db['tb_vl_col']] =
                        $this->sessDecrypt($_row[$this->_db['tb_vl_col']],
                                           $_row[$this->_db['tb_iv_col']],
                                           TRUE);
                }


            }

            if (is_array($_row)) {
                if ($this->_MAGIC_QUOTES_RUNTIME) {
                    $_row[$this->_db['tb_si_col']] =
                        stripslashes($_row[$this->_db['tb_si_col']]);

                    $_row[$this->_db['tb_tr_col']] =
                        stripslashes($_row[$this->_db['tb_tr_col']]);

                }

                return $_row;

            } else {

                return FALSE;

            }

        }
    }


    /**
     * getAllSessInfo - This will return column information for the number of
     * rows indicated (default is to return all rows). You can select the
     * column to sort by (expiry is the default) and whether to sort by
     * ascending or descending (default) sort order. It returns a two
     * dimensional associative array. The first array index is the row number,
     * and the second array index is the table column names.
     * The session data value, and encryption IV column values are returned
     * only when a confirm password is passed. If the session value is
     * encrypted, it will automatically be decrypted, however the session
     * value data will be raw (in serialized format).
     * The other columns retrieved are useful for determining when a session
     * was created/started and when it will expire.
     *
     * The trace column can be split into individual values. For example:
     * $data = $sess->getAllSessInfo();
     * $arr  = explode('~', $data[0]['sess_trace']); // $arr[1] is IP Address
     *
     * You can use PHP's getdate() function to convert the columns that contain
     * epoch values (such as session created, expiry, and timeout).
     * @link   http://us4.php.net/manual/en/function.getdate.php
     *
     * @param  int    $_offset The row number to start returning data from
     * @param  int    $_row_count The number of rows to return (-1 = all rows).
     * @param  string $_order_by The column name to sort rows by (def=expiry).
     * @param  bool   $_ascending Ascending or descending sort order (def=desc)
     * @param  string $_confirmation_pswd Pass to retrieve raw session value.
     * @return mixed  Returns a 2D array of data or FALSE on error/no data.
     * @access public
     */
    function getAllSessInfo($_offset = 0,
                            $_row_count = -1,
                            $_order_by = NULL,
                            $_ascending = FALSE,
                            $_confirmation_pswd = NULL)
    {

        if (!is_int($_offset))
            $_offset = (int) 0;

        if ($_offset < 0)
            $_offset = (int) 0;

        if (!is_int($_row_count))
            $_row_count = (int) -1;

        if (0 == $_row_count)
            $_row_count = (int) -1;

        if (empty($_order_by))
            $_order_by = $this->_db['tb_ex_col'];
        else
            if (($_order_by != $this->_db['tb_id_col']) &&
                ($_order_by != $this->_db['tb_sl_col']) &&
                ($_order_by != $this->_db['tb_cr_col']) &&
                ($_order_by != $this->_db['tb_ex_col']) &&
                ($_order_by != $this->_db['tb_to_col']) &&
                ($_order_by != $this->_db['tb_lk_col']) &&
                ($_order_by != $this->_db['tb_vl_col']) &&
                ($_order_by != $this->_db['tb_iv_col']) &&
                ($_order_by != $this->_db['tb_si_col']) &&
                ($_order_by != $this->_db['tb_tr_col']))
                 $_order_by = $this->_db['tb_ex_col'];

        if (!is_bool($_ascending))
            $_ascending = FALSE;

        $_asc_desc = (TRUE === $_ascending) ? 'ASC' : 'DESC';

        /**
         * Verify that raw session value is requested to be retrieved as well
         * by checking the passed password against the confirm password
         * defined in _param['confirm_pswd']
         */
        $_pswd_valid = (0 === strcmp($_confirmation_pswd, $this->_CONF_PSWD)) ?
                        TRUE : FALSE;

        $_sql  = 'SELECT '    . $this->_db['tb_id_col'] .
                         ', ' . $this->_db['tb_sl_col'] .
                         ', ' . $this->_db['tb_cr_col'] .
                         ', ' . $this->_db['tb_ex_col'] .
                         ', ' . $this->_db['tb_to_col'] .
                         ', ' . $this->_db['tb_lk_col'] .
                         ', ' . $this->_db['tb_si_col'] .
                         ', ' . $this->_db['tb_tr_col'];

        if ($_pswd_valid)
            $_sql  .=    ', ' . $this->_db['tb_vl_col'] .
                         ', ' . $this->_db['tb_iv_col'];

        $_sql .= '  FROM '  . $this->_db['tb_name']     .
                 " ORDER BY $_order_by $_asc_desc LIMIT $_offset,$_row_count";

        $_result = @mysql_query($_sql, $this->_dbh);

        if (!$_result) {

            // All session information query failed.
            $this->_setErrMsg('ALL_INFO_FAIL', $_sql);
            $this->_handleErrors();

            return FALSE;

        } else {

            $_rows = array();

            while ($_row = @mysql_fetch_assoc($_result)) {


                if ($_pswd_valid) {

                    $_row[$this->_db['tb_vl_col']] =
                        isSet($_row[$this->_db['tb_vl_col']]) ?
                              $_row[$this->_db['tb_vl_col']]  : '';

                    $_row[$this->_db['tb_iv_col']] =
                        isSet($_row[$this->_db['tb_iv_col']]) ?
                            $_row[$this->_db['tb_iv_col']]  : '';

                    if ($this->_MAGIC_QUOTES_RUNTIME) {
                        $_row[$this->_db['tb_vl_col']] =
                            stripslashes($_row[$this->_db['tb_vl_col']]);

                        $_row[$this->_db['tb_iv_col']] =
                            stripslashes($_row[$this->_db['tb_iv_col']]);
                    }

                    /**
                     * Decrypt the data if it was encrypted
                     */
                    if ((!empty($_row[$this->_db['tb_iv_col']])) &&
                        (!empty($_row[$this->_db['tb_vl_col']]))) {

                        $_row[$this->_db['tb_vl_col']] =
                            $this->sessDecrypt($_row[$this->_db['tb_vl_col']],
                                               $_row[$this->_db['tb_iv_col']],
                                               TRUE);
                    }


                }


                if ($this->_MAGIC_QUOTES_RUNTIME) {
                    $_row[$this->_db['tb_si_col']] =
                        stripslashes($_row[$this->_db['tb_si_col']]);

                    $_row[$this->_db['tb_tr_col']] =
                        stripslashes($_row[$this->_db['tb_tr_col']]);

                }

                $_rows[] = $_row;

            }

            if (count($_rows) > 0) {

                @mysql_free_result($_result);
                return $_rows;

            } else {
                // Warning: No session data found while doing all session query
                $this->_setWrnMsg('NO_SESS_INFO2', $_sql);
                $this->_handleErrors();
                return FALSE;

            }


        }
    }


    /**
     * getTableName - Returns the name of the session table.
     *
     * @return string Returns the MySQL table name
     * @access public
     */
    function getTableName()
    {
        return $this->_db['tb_name'];
    }


    /**
     * getSessIDName - Returns the name of the session ID (key) column.
     *
     * @return string Returns the MySQL table column name for session ID
     * @access public
     */
    function getSessIDName()
    {
        return $this->_db['tb_id_col'];
    }


    /**
     * getSecLevelName - Returns the name of the security level column.
     *
     * @return string Returns the MySQL table column name for security level
     * @access public
     */
    function getSecLevelName()
    {
        return $this->_db['tb_sl_col'];
    }


    /**
     * getCreateName - Returns the name of the session created column.
     *
     * @return string Returns the MySQL table column name for created epoch.
     * @access public
     */
    function getCreateName()
    {
        return $this->_db['tb_cr_col'];
    }


    /**
     * getExpiryName - Returns the name of the session expiry column.
     *
     * @return string Returns the MySQL table column name for expiry epoch.
     * @access public
     */
    function getExpiryName()
    {
        return $this->_db['tb_ex_col'];
    }


    /**
     * getTimeoutName - Returns the name of the session timeout column.
     *
     * @return string Returns the MySQL table column name for timeout epoch.
     * @access public
     */
    function getTimeoutName()
    {
        return $this->_db['tb_to_col'];
    }


    /**
     * getLockName - Returns the name of the session locked column.
     *
     * @return string Returns the MySQL table column name for locked boolean.
     * @access public
     */
    function getLockName()
    {
        return $this->_db['tb_lk_col'];
    }


    /**
     * getSessValueName - Returns the name of the session value column.
     *
     * @return string Returns the MySQL table column name for session value.
     * @access public
     */
    function getSessValueName()
    {
        return $this->_db['tb_vl_col'];
    }


    /**
     * getEncIVName - Returns the name of the encryption IV column.
     *
     * @return string Returns the MySQL table column name for encryption IV.
     * @access public
     */
    function getEncIVName()
    {
        return $this->_db['tb_iv_col'];
    }


    /**
     * getSecIDName - Returns the name of the security ID column.
     *
     * @return string Returns the MySQL table column name for security ID.
     * @access public
     */
    function getSecIDName()
    {
        return $this->_db['tb_si_col'];
    }


    /**
     * getTraceName - Returns the name of the session trace column.
     *
     * @return string Returns the MySQL table column name for session trace.
     * @access public
     */
    function getTraceName()
    {
        return $this->_db['tb_tr_col'];
    }


    /**
     * nbrActiveSess - Retrieves the number of active sessions currently in the
     * table.
     *
     * @return int    The number of session rows that are considered active.
     * @access public
     */
    function nbrActiveSess()
    {

        $_time = time();

        $_sql  = 'SELECT '  . $this->_db['tb_lk_col']  .
                 '  FROM '  . $this->_db['tb_name']    .
                 ' WHERE (' . $this->_db['tb_ex_col']  . " > '$_time')" .
                 '   AND (' . $this->_db['tb_to_col']  . " > '$_time')" .
                 '   AND (' . $this->_db['tb_lk_col']  . " = '0')";

        $_result = @mysql_query($_sql, $this->_dbh);

        if (!$_result) {

            // Active sessions query failed. Could not read session data
            $this->_setErrMsg('ACTIVE_FAIL', $_sql);
            $this->_handleErrors();

            return (bool) FALSE;                // Return an error

        } else {

            return @mysql_num_rows($_result);

        }
    }


    /**
     * nbrInactiveSess - Retrieves the number of inactive sessions currently in
     * the table.
     *
     * @return int     The number of session rows that are considered inactive.
     * @access public
     */
    function nbrInactiveSess()
    {

        $_time = time();

        $_sql  = 'SELECT '  . $this->_db['tb_lk_col']  .
                 '  FROM '  . $this->_db['tb_name']    .
                 ' WHERE (' . $this->_db['tb_ex_col']  . " < '$_time')" .
                 '    OR (' . $this->_db['tb_to_col']  . " < '$_time')" .
                 '    OR (' . $this->_db['tb_lk_col']  . " = '1')";

        $_result = @mysql_query($_sql, $this->_dbh);

        if (!$_result) {

            // Inactive sessions query failed. Could not read session data
            $this->_setErrMsg('INACTIVE_FAIL', $_sql);
            $this->_handleErrors();

            return (bool) FALSE;                // Return an error

        } else {

            return @mysql_num_rows($_result);

        }
    }


    /**
     * changeSessLock - To lock or unlock a session row in the table.
     * When a session is locked, it will not be further read and is considered
     * temporarily or permanently suspended.
     * Must pass a valid session ID; no default assigned.
     * Note: MySQL will not update columns where the new value is the same as
     * the old value.
     *
     * @param  string  $_sess_id Session ID of the row to change the lock on.
     * @param  bool    $_lock_mode Set to TRUE for lock and FALSE for unlock.
     * @return bool    TRUE on a successful lock/unlock, and FALSE on error or
     *                 empty session string.
     * @access public
     */
    function changeSessLock($_sess_id, $_lock_mode = FALSE)
    {

        if (empty($_sess_id))
            return FALSE;

        if (!is_bool($_lock_mode))
            $_lock_mode = FALSE;

        if (TRUE === $_lock_mode)
            $_lock_mode = 1;
        else
            $_lock_mode = 0;


        $_sql = 'UPDATE ' . $this->_db['tb_name']     .
                  ' SET '                             .
                            $this->_db['tb_lk_col']   .
                            "='$_lock_mode'"          .
                ' WHERE ' . $this->_db['tb_id_col']   .
                            " = '$_sess_id'";


        $_result = @mysql_query($_sql, $this->_dbh);

        if (!$_result) {
            // Lock/unlock failed. Could not change session data
            $this->_setErrMsg('A_LOCK_FAIL', $_sql, $_sess_id);
            $this->_handleErrors();
        }

        return (bool) $_result;
    }


    /**
     * changeAllSessLocks - To lock or unlock all session rows in the table.
     * When a session is locked, it will not be further read and is considered
     * temporarily or permanently suspended. Pass the _param['confirm_pswd']
     * to this member function as a way of making sure that it is the intention
     * to lock/unlock all rows in the session table.
     * Note: MySQL will not update columns where the new value is the same as
     * the old value.
     *
     * @param  string  $_confirmation_pswd Password required to change all rows.
     * @param  bool    $_lock_mode Set to TRUE for lock and FALSE for unlock.
     * @return bool    TRUE when rows are successfully locked/unlocked, or FALSE
     *                 on error or invalid password supplied.
     * @access public
     */
    function changeAllSessLocks($_confirmation_pswd = NULL, $_lock_mode = FALSE)
    {

        /**
         * Verify lock/unlock request by checking the passed password against
         * the confirm password defined in _param['confirm_pswd']
         */
        if (0 !== strcmp($_confirmation_pswd, $this->_CONF_PSWD))
            return FALSE;

        if (!is_bool($_lock_mode))
            $_lock_mode = FALSE;

        if (TRUE === $_lock_mode)
            $_lock_mode = 1;
        else
            $_lock_mode = 0;


        $_sql = 'UPDATE ' . $this->_db['tb_name']     .
                  ' SET ' . $this->_db['tb_lk_col']   .
                            "='$_lock_mode'";

        $_result = @mysql_query($_sql, $this->_dbh);

        if (!$_result) {
            // Lock/unlock failed. Could not change all the session data
            $this->_setErrMsg('ALL_LOCK_FAIL', $_sql);
            $this->_handleErrors();
        }

        return (bool) $_result;
    }


    /**
     * deleteSession - To manually delete an old/expired session row from the
     * table. Must pass a valid session ID; no default assigned.
     *
     * @param  string  $_sess_id Session ID of the row to delete.
     * @return bool    TRUE on a successful delete, and FALSE on error or empty
     *                 session string.
     * @access public
     */
    function deleteSession($_sess_id)
    {

        if (empty($_sess_id))
            return FALSE;

        /**
         * When session ID is the same as the current one, then use
         * session_destroy() to delete a current active session
         * instead of this method.
         */
        if (0 === strcmp($_sess_id, session_id()))
            return session_destroy();

        $_sql = 'DELETE FROM ' . $this->_db['tb_name'] .
                     ' WHERE ' . $this->_db['tb_id_col']  .
                                 " = '$_sess_id'";

        $_result = @mysql_query($_sql, $this->_dbh);

        if (!$_result) {
            // Delete request failed. Could not delete session data
            $this->_setErrMsg('A_DEL_FAIL', $_sql, $_sess_id);
            $this->_handleErrors();
        }

        return (bool) $_result;
    }


    /**
     * deleteAllSessions - To delete all session rows from table. It's faster
     * to drop and create the table again, however, the current database user
     * should not have such security privileges. Pass the _param['confirm_pswd']
     * to this member function as a way of making sure that it is the intention
     * to delete all rows from the session table.
     *
     * @param  string  $_confirmation_pswd Password required to delete all rows.
     * @return bool    TRUE when rows are successfully deleted, and FALSE on
     *                 error or invalid password supplied.
     * @access public
     */
    function deleteAllSessions($_confirmation_pswd = NULL)
    {

        /**
         * Verify delete request by checking the passed password against
         * the confirm password defined in _param['confirm_pswd']
         */
        if (0 !== strcmp($_confirmation_pswd, $this->_CONF_PSWD))
            return FALSE;

        $_sql = 'DELETE FROM ' . $this->_db['tb_name'];

        $_result = @mysql_query($_sql, $this->_dbh);

        if (!$_result) {
            // Delete all request failed. Could not delete all session data
            $this->_setErrMsg('ALL_DEL_FAIL', $_sql);
            $this->_handleErrors();
        }

        return (bool) $_result;
    }


    /**
     * pregMatches - Returns a boolean of a whole word preg_match result. It
     * checks $_pattern against $_value and returns a boolean result. The
     * preg_match result must match $_value for it to return a TRUE result.
     * It uses a default pattern of '/[a-zA-Z0-9]+/' when no pattern is
     * specified.
     *
     * @param  string $_pattern Set to a valid regular expression pattern.
     * @param  string $_value Set to a value to have the $_pattern check against
     * @return bool Returns TRUE when $_pattern is found in $_value.
     * @access public
     */
    function pregMatches($_pattern, $_value)
    {
        if (empty($_pattern))
            $_pattern = '/[a-zA-Z0-9]+/';  // Match this pattern 1 or more times

        $_matches = array();

        if (preg_match($_pattern, $_value, $_matches) > 0)
            if (0 === @strcmp($_value, $_matches[0]))
                return TRUE;

        return FALSE;

    }


    /**
     * stringSplit - Parses out a string into x number of byte chunk characters.
     * Example: $arr = stringSplit('Hi', 1);
     *
     * $arr then contains: $arr[0] = 'H'  and  $arr[1] = 'i'
     *
     * @param  string $_text Pass a text string you would like to parse out.
     * @param  int    $_chunksize The number of characters to split by.
     * @return array  Returns an array with each index containing x characters.
     * @access public
     */
    function stringSplit($_text, $_chunksize = 1)
    {
        preg_match_all('/(' . str_repeat('.', $_chunksize) . ')/Uims',
                       $_text,
                       $_matches);

        return $_matches[1];
    }


    /**
     * sessEncode - Encrypts plain text. It uses an Initialization Vector (IV)
     * integer in the range of 1-500 in order to produce more varied results.
     * You must use the same IV number when calling the sessDecode member.
     * The encrypted text may be longer than original plain text.
     * This function requires PHP ver >= 4.2.0 because of str_rot13 function.
     *
     *
     * @param  string $_text Pass the plain text you would like to encrypt.
     * @param  int    $_IV Pass a random number between 1 and 500.
     * @return string Returns the plain text passed in encrypted format.
     * @access public
     */
    function sessEncode($_text, $_IV = 3)
    {

        if (is_numeric($_IV)) {

            $_IV = intval($_IV);

            if ($_IV < 1)
                $_IV = 1;
            else
              if ($_IV > 500)
                  $_IV = 42;

        } else {

            $_IV = 3;
        }

        $_text .= ' ';

        $_arr1 = $this->stringSplit($this->_ENCRYPT_KEY);
        $_arr2 = $_arr1;

        foreach ($_arr1 as $_i1 => $_v1) {

            foreach ($_arr2 as $_i2 => $_v2) {

                $_counter = ($_i2 + 1) + ($_i1 * strlen($this->_ENCRYPT_KEY));

                $_array[$_counter] = $_v1 . $_v2;

                if ($_v1 == $_v2)
                    $_array[$_counter] = $_v1 . '_';
            }
        }

        $_encoded = '';
        $_count = 0;
        $_msgarr = $this->stringSplit($_text);

        foreach ($_msgarr as $_mindex => $_mvalue) {

            If ($_mindex / 2 <> ceil ($_mindex / 2)) {

                $_masc = ord($_mvalue) - 31;
                $_masc = $_masc + (ceil($_count * $_IV / 3) + $_IV);
                $_count++;
                if ($_count > 12)
                    $_count = 0;
                $_encoded .= $_array[$_masc];

            } else {

                // No need to get around str_rot13 bug here since $_mvalue is
                // not being referenced after this point & will get overriden.
                $_encoded .= str_rot13($_mvalue);
            }
        }

        return $_encoded;
    }


    /**
     * sessDecode - Decodes text that was previously encrypted with sessEncode.
     * This function requires PHP ver >= 4.2.0 because of str_rot13 function.
     *
     * @param  string $_text Pass the encrypted text created by sessEncode.
     * @param  int    $_IV Pass the same IV number as used in sessEncode.
     * @return string Returns the unencrypted plain text.
     * @access public
     */
    function sessDecode($_text, $_IV = 3)
    {

        $_count = 0;

        if (is_numeric($_IV)) {

            $_IV = intval($_IV);

            if ($_IV < 1)
                $_IV = 1;
            else
              if ($_IV > 500)
                  $_IV = 42;

        } else {

            $_IV = 3;
        }

        $_arr1 = $this->stringSplit($this->_ENCRYPT_KEY);
        $_arr2 = $_arr1;

        foreach ($_arr1 as $_i1 => $_v1) {

            foreach ($_arr2 as $_i2 => $_v2) {

                $_counter = ($_i2 + 1) + ($_i1 * strlen($this->_ENCRYPT_KEY));
                $_array[$_counter] = $_v1 . $_v2;
                if ($_v1 == $_v2)
                    $_array[$_counter] = $_v1 . '_';
            }
        }

        $_array = array_flip($_array);
        $_msgarr = $this->stringSplit($_text, 3);

        $_decoded = '';            // Rev 1.0.2: Added this initialization line

        foreach ($_msgarr as $_mvalue) {

            // $_tmp_hold used to get around a possible PHP bug in versions
            // earlier than 4.3.0. The variable passed in function might change.
            $_tmp_hold  = $_mvalue;
            $_decoded  .= str_rot13($_tmp_hold{0});

            $_ivalue = $_array[substr($_mvalue, 1, 2)];
            $_ivalue = $_ivalue - (ceil($_count * $_IV / 3) + $_IV);
            $_count++;
            if ($_count > 12)
                $_count = 0;

            $_masc = chr($_ivalue + 31);
            $_decoded .= $_masc;
        }

        return trim($_decoded);    // Rev 1.0.1: Added trim(). Removed substr().
    }


    /**
     * sessEncrypt - Encrypts plain text. It uses an Initialization Vector (IV).
     * The same IV is needed for the decryption phase. Must save IV for
     * later decryption. This routine will attempt to use the mcrypt
     * algorithms if installed first, otherwise the sessEncode member is used.
     * The encrypted text may be longer than original plain text. When you have
     * a few/many fields to encrypt in one script cycle, choose to keep the
     * mcrypt module open to speed up encryption (only for libmcrypt >= 2.4.x).
     *
     * @link   http://mcrypt.hellug.gr
     * @param  string $_text Pass the plain text you would like to encrypt.
     * @param  string $IV Pass by reference var. This will get assigned the IV.
     * @param  bool   $_keep_open TRUE to keep mcrypt module open, FALSE close.
     * @return mixed  Returns an encrypted value representing the original
     *                text, or FALSE on error.
     * @access public
     */
    function sessEncrypt($_text, &$IV, $_keep_open = FALSE)
    {

        static $_open_already = FALSE;  // Open encrypt flag For ver >= 2.4.x
        static $_module       = NULL;


        if (!is_bool($_keep_open))
            $_keep_open = FALSE;

        if (($this->_MCRYPT) &&
            (!empty($this->_ENC_ALGO)) &&
            (!empty($this->_ENC_MODE))) {

            if ($this->_MCRYPT_LATEST) {    // For >= 2.4.x

                if (!$_open_already) {

                    $_module = @mcrypt_module_open($this->_ENC_ALGO, '',
                                                   $this->_ENC_MODE, '');

                    if (FALSE === $_module) {

                        // Could not open encryption module for encrypting
                        $this->_setErrMsg('ENC_OPEN_FAIL', NULL,
                                          $this->_ENC_ALGO, $this->_ENC_MODE);
                        $this->_handleErrors();

                        return FALSE;

                    }

                    $_open_already = TRUE;

                }

                $IV = @mcrypt_create_iv (@mcrypt_enc_get_iv_size($_module),
                                         MCRYPT_RAND);   // For Windows support

                $_key = substr($this->_ENC_KEY_HASHED, 0,
                               @mcrypt_enc_get_key_size($_module));

                $_result = mcrypt_generic_init($_module, $_key, $IV);

                if ($_result < 0) {

                    switch ($_result) {

                        case -3:

                            // Key length for encryption is incorrect
                            $this->_setErrMsg('ENC_KEY_LEN', NULL,
                                              $this->_ENC_ALGO,
                                              $this->_ENC_MODE,
                                              strlen($_key));

                        case -4:

                            // There were memory allocation problems - encrypt
                            $this->_setErrMsg('ENC_MEMORY', NULL,
                                              $this->_ENC_ALGO,
                                              $this->_ENC_MODE);

                        default:

                            // There were unknown errors while trying to encrypt
                            $this->_setErrMsg('ENC_UNKNOWN', NULL,
                                              $this->_ENC_ALGO,
                                              $this->_ENC_MODE);

                    }

                    $this->_handleErrors();

                    return FALSE;
                }

                $_enc = @mcrypt_generic($_module, $_text);


                if (!$_keep_open) {

                    @mcrypt_generic_deinit($_module);
                    @mcrypt_module_close($_module);

                    $_open_already = FALSE;
                    $_module = NULL;
                }


            } else {    // For 2.2.x

                $IV   = @mcrypt_create_iv(
                                          @mcrypt_get_block_size(
                                                                $this->_ENC_ALGO
// FYI: Would be needed to run in > 2.2.x                     , $this->_ENC_MODE
                                                                ),
                                          MCRYPT_RAND
                                         ); // MCRYPT_RAND for Windows support

                $_key = substr($this->_ENC_KEY_HASHED, 0,
                               @mcrypt_get_key_size($this->_ENC_ALGO
// FYI: Would be needed to run in > 2.2.x         , $this->_ENC_MODE
                                                   )
                              );

                switch ($this->_ENC_MODE) {

                     case MCRYPT_MODE_ECB:

                     $_enc = @mcrypt_ecb(
                                         $this->_ENC_ALGO,
                                         $_key,
                                         $_text,
                                         MCRYPT_ENCRYPT
// FYI: Would be needed to run in > 2.2.x , $IV
                                        );

                     $IV   = '';        // FYI: Would comment to run in > 2.2.x
                     break;

                     case MCRYPT_MODE_CFB:

                     $_enc = @mcrypt_cfb(
                                         $this->_ENC_ALGO,
                                         $_key,
                                         $_text,
                                         MCRYPT_ENCRYPT,
                                         $IV
                                        );
                     break;

                     case MCRYPT_MODE_OFB:

                     $_enc = @mcrypt_ofb(
                                         $this->_ENC_ALGO,
                                         $_key,
                                         $_text,
                                         MCRYPT_ENCRYPT,
                                         $IV
                                        );
                     break;

                     default:

                     $_enc = @mcrypt_cbc(
                                         $this->_ENC_ALGO,
                                         $_key,
                                         $_text,
                                         MCRYPT_ENCRYPT,
                                         $IV
                                        );
                }

            }

            $_enc = trim(@base64_encode($_enc));
            $IV   = trim(@base64_encode($IV));

        } else {

            $IV   = (int) mt_rand(1, 500);

            $_enc = $this->sessEncode($_text, $IV);

        }

        return $_enc;

    }


    /**
     * sessDecrypt - Decrypts encrypted text created by the sessEncrypt member.
     * It needs to be passed the same Initialization Vector (IV) used in the
     * encryption process. When you have a few/many fields to decrypt in one
     * script cycle, choose to keep the mcrypt module open to speed up
     * decryption (only for libmcrypt >= 2.4.x). A correctly decrypted field
     * will be returned as a string, so if you're expecting/wanting an integer
     * then you have to type cast or use intval() function.
     *
     * @param  string $_enc Pass the encrypted text you would like to decrypt.
     * @param  string $_IV Pass the same IV used in the encryption phase.
     * @param  bool   $_keep_open TRUE to keep mcrypt module open, FALSE close.
     * @return mixed  Returns the original plain text or FALSE on error.
     * @access public
     */
    function sessDecrypt($_enc, $_IV, $_keep_open = FALSE)
    {

        static $_open_already = FALSE;  // Open encrypt flag For ver >= 2.4.x
        static $_module       = NULL;


        if (!is_bool($_keep_open))
            $_keep_open = FALSE;


        if ((is_numeric($_IV))  &&
            (strlen($_IV) > 0)  &&
            (strlen($_IV) < 4)  &&
            (intval($_IV) > 0)  &&
            (intval($_IV) < 501)) {

            $_text = $this->sessDecode($_enc, intval($_IV));

        } else
        if (($this->_MCRYPT) &&
            (!empty($this->_ENC_ALGO)) &&
            (!empty($this->_ENC_MODE))) {

            $_IV   = @base64_decode($_IV);
            $_enc  = @base64_decode($_enc);

            if ($this->_MCRYPT_LATEST) {    // For >= 2.4.x

                if (!$_open_already) {

                    $_module = @mcrypt_module_open($this->_ENC_ALGO, '',
                                                   $this->_ENC_MODE, '');

                    if (FALSE === $_module) {

                        // Could not open encryption module for decryption
                        $this->_setErrMsg('DEC_OPEN_FAIL', NULL,
                                          $this->_ENC_ALGO, $this->_ENC_MODE);
                        $this->_handleErrors();

                        return FALSE;

                    }

                    $_open_already = TRUE;
                }

                $_key = substr($this->_ENC_KEY_HASHED, 0,
                               @mcrypt_enc_get_key_size($_module));

                $_result = @mcrypt_generic_init($_module, $_key, $_IV);

                if ($_result < 0) {

                    switch ($_result) {

                        case -3:

                            // Key length for decryption is incorrect
                            $this->_setErrMsg('DEC_KEY_LEN', NULL,
                                              $this->_ENC_ALGO,
                                              $this->_ENC_MODE,
                                              strlen($_key));

                        case -4:

                            // There were memory allocation problems - decrypt
                            $this->_setErrMsg('DEC_MEMORY', NULL,
                                              $this->_ENC_ALGO,
                                              $this->_ENC_MODE);

                        default:

                            // There were unknown errors while trying to decrypt
                            $this->_setErrMsg('DEC_UNKNOWN', NULL,
                                              $this->_ENC_ALGO,
                                              $this->_ENC_MODE);

                    }

                    $this->_handleErrors();

                    return FALSE;
                }

                // trim is especially needed in Cipher Block Chaining (CBC) mode
                $_text = trim(@mdecrypt_generic($_module, $_enc));

                if (!$_keep_open) {

                    @mcrypt_generic_deinit($_module);
                    @mcrypt_module_close($_module);

                    $_open_already = FALSE;
                    $_module = NULL;
                }

            } else {            // For 2.2.x


                $_key = substr($this->_ENC_KEY_HASHED, 0,
                               @mcrypt_get_key_size($this->_ENC_ALGO
// FYI: Would be needed to run in > 2.2.x          ,$this->_ENC_MODE
                                                   )
                              );

                switch ($this->_ENC_MODE) {

                     case MCRYPT_MODE_ECB:

                     $_text = @mcrypt_ecb(
                                          $this->_ENC_ALGO,
                                          $_key,
                                          $_enc,
                                          MCRYPT_DECRYPT
// FYI: Would be needed to run in > 2.2.x ,$_IV
                                         );

                     break;

                     case MCRYPT_MODE_CFB:

                     $_text = @mcrypt_cfb(
                                          $this->_ENC_ALGO,
                                          $_key,
                                          $_enc,
                                          MCRYPT_DECRYPT,
                                          $_IV
                                         );
                     break;

                     case MCRYPT_MODE_OFB:

                     $_text = @mcrypt_ofb(
                                          $this->_ENC_ALGO,
                                          $_key,
                                          $_enc,
                                          MCRYPT_DECRYPT,
                                          $_IV
                                         );
                     break;

                     default:

                     $_text = @mcrypt_cbc(
                                          $this->_ENC_ALGO,
                                          $_key,
                                          $_enc,
                                          MCRYPT_DECRYPT,
                                          $_IV
                                         );
                }

                $_text = trim($_text); // Especially needed for CBC mode

            }

        } else {

            $_text = FALSE;

        }

        return $_text;
    }


    /**
     * sendCacheHeader - Transmits the value for the Cache-Control header
     * option(s).
     *
     * @uses   Example to stop caching: 'no-store, no-cache, must-revalidate,
     *                                   post-check=0, pre-check=0'
     *
     * @param  string $_options Cache-Control header option(s)
     * @return bool   Always returns TRUE.
     * @access public
     */
    function sendCacheHeader($_options = 'private')
    {

        header("Cache-Control: $_options");

        return TRUE;
    }


    /**
     * getMySQLVer - Call to obtain the version number of the MySQL server.
     *
     * @return string Returns the current MySQL server version number.
     * @access public
     */
    function getMySQLVer()
    {
        return $this->_mysql_ver;
    }


    /**
     * getSessName - Call to obtain the current PHP Session name (used in URL's)
     *
     * @return string Returns the current PHP Session name.
     * @access public
     */
    function getSessName()
    {
        return $this->_sess_name;
    }


    /**
     * getSessLife - Retrieves the current PHP Session life duration. Set
     * $_in_minutes to TRUE to return a value in minutes (rounded up to
     * the next whole minute).
     *
     * @param  bool   $_in_minutes A switch to signify that the return value
     *                should be in minutes instead of seconds (the default).
     * @return int    Returns the number of seconds or minutes of session life.
     * @access public
     */
    function getSessLife($_in_minutes = FALSE)
    {
        if ($_in_minutes)
            return intval(ceil($this->_SESS_LIFE / 60));
        else
            return (int) $this->_SESS_LIFE;
    }


    /**
     * getSessTimeout - Returns what the session timeout duration is set to. Set
     * $_in_minutes to TRUE to return a value in minutes (rounded up to
     * the next whole minute).
     *
     * @param  bool   $_in_minutes A switch to signify that the return value
     *                should be in minutes instead of seconds (the default).
     * @return int    Returns the number of seconds/minutes of session timeout.
     * @access public
     */
    function getSessTimeout($_in_minutes = FALSE)
    {
        if ($_in_minutes)
            return intval(ceil($this->_SESS_TIMEOUT / 60));
        else
            return (int) $this->_SESS_TIMEOUT;
    }


    /**
     * setSessVar - Creates or updates a session variable's value. You can
     * select to have the session variables contents be encrypted. For extra
     * security, you can select for an extra/duplicate field to be created which
     * will contain the encrypted value (while leaving the non-encrypted value
     * in the session field specified untouched). By using this option,
     * getSessVar() will automatically make a comparison of the two values for
     * extra validity. For the encryption option, the value can't be an array,
     * a boolean, a resource, or an object.
     *
     * @param  string $_field Name to assign as key index in $_SESSION array.
     * @param  mixed  $_value to assign the field name/key in $_SESSION array.
     * @param  bool   $_encrypt_value Set TRUE to have encryption performed.
     * @param  bool   $_extra_field Set TRUE to create a new encrypted field.
     * @param  string $_ENC_SFX Encrypted field suffix value added to create
     *                the new encrypted field.
     * @param  string $_ENC_IV_SFX The IV field suffix value added to create
     *                the IV field. Always created with encryption option.
     * @param  bool   $_ERROR Set to what value should be returned upon error.
     * @return bool   Returns TRUE when field value is set, FALSE on NULL/error.
     * @access public
     */
    function setSessVar($_field,
                        $_value         = NULL,
                        $_encrypt_value = FALSE,
                        $_extra_field   = FALSE,
                        $_ENC_SFX       = '_enc',
                        $_ENC_IV_SFX    = '_enc_iv',
                        $_ERROR         = FALSE
                       )

    {

        if (empty($_field))
            return $_ERROR;

        if (!is_bool($_encrypt_value))
            $_encrypt_value = FALSE;

        /**
         * When encryption requested, see if we can encrypt this type of value.
         */
        if (($_encrypt_value)       &&
            (!is_array($_value))    &&
            (!is_bool($_value))     &&
            (!is_resource($_value)) &&
            (!is_object($_value)))  {

            $_enc_iv = 0;

            $_enc = $this->sessEncrypt($_value, $_enc_iv, TRUE);

            if (FALSE === $_enc)
                return $_ERROR;               // Encryption didn't work

            if (!$this->pregMatches('/[a-zA-Z0-9_]+/', $_ENC_IV_SFX))
                $_ENC_IV_SFX = '_enc_iv';

            /**
             * Save encrypted info.
             */
            $_SESSION[$_field . $_ENC_IV_SFX] = $_enc_iv;

            if (!is_bool($_extra_field))
                $_extra_field = FALSE;

            if ($_extra_field) {

                if (!$this->pregMatches('/[a-zA-Z0-9_]+/', $_ENC_SFX))
                    $_ENC_SFX = '_enc';

                /**
                 * Place encrypted value in a new field, and leave non-encrypted
                 * value in selected/same field.
                 */
                $_SESSION[$_field . $_ENC_SFX] = $_enc;
                $_SESSION[$_field] = $_value;

            } else {

                /**
                 * No extra field wanted, so place encrypted value in
                 * selected/same field.
                 */
                $_SESSION[$_field] = $_enc;
            }


        } else {    // Encryption not requested or not right type

            $_SESSION[$_field] = $_value;
        }

        return isSet($_SESSION[$_field]);
    }


    /**
     * getSessVar - Returns a session variables value if assigned (and not NULL)
     * or the default value supplied, or NULL when no default supplied. Also,
     * this will detect if a value had been encrypted and will automatically
     * return the decrypted value. When the extra field option is used in
     * setSessVar(), then a comparison of original and extra field values are
     * automatically performed to make sure that the original fields value has
     * not been modified by an outside source (hacker).
     * FYI: The $_SESSION array is only made available after a session_start().
     *
     * @param  string $_field Key name to look for in $_SESSION superglobal
     *                array.
     * @param  mixed  $_default A value to return when var is not set/NULL.
     * @param  string $_ENC_SFX Encrypted field suffix value used when
     *                encryption field was created (in setSessVar).
     * @param  string $_ENC_IV_SFX The IV field suffix value used when the IV
     *                field was created (in setSessVar).
     * @param  bool   $_ERROR Set to what value should be returned upon error.
     * @return mixed  Returns session variable value, assigned default, or
     *                FALSE on error.
     * @access public
     */
    function getSessVar($_field,
                        $_default    = NULL,
                        $_ENC_SFX    = '_enc',
                        $_ENC_IV_SFX = '_enc_iv',
                        $_ERROR      = FALSE
                       )
    {

        if (empty($_field))
            return $_ERROR;

        /**
         * Determine if field has already been defined
         */
        if (isSet($_SESSION[$_field])) {

            if (!$this->pregMatches('/[a-zA-Z0-9_]+/', $_ENC_IV_SFX))
                $_ENC_IV_SFX = '_enc_iv';

            /**
             * When this field is defined we have an encrypted value
             */
            $_enc_iv = (isSet($_SESSION[$_field . $_ENC_IV_SFX])) ?
                              $_SESSION[$_field . $_ENC_IV_SFX]   : NULL;

            /**
             * It's not encrypted when there's no IV value defined
             */
            if (is_null($_enc_iv)) {

                return $_SESSION[$_field];      // Return non-encrypted value

            }

            if (!$this->pregMatches('/[a-zA-Z0-9_]+/', $_ENC_SFX))
                $_ENC_SFX = '_enc';

            /**
             * We now know that we have an encrypted value. Find out if the
             * original or the extra field contains the encrypted value.
             */
            $_enc = (isSet($_SESSION[$_field . $_ENC_SFX])) ?
                           $_SESSION[$_field . $_ENC_SFX]   :
                           $_SESSION[$_field];

            $_text = $this->sessDecrypt($_enc, $_enc_iv, TRUE);

            if (FALSE === $_text)
                return $_ERROR;                   // Error with decryption

           /**
             * If the extra field contained the encrypted value, then compare
             * the original fields value with the decrypted value. They should
             * both match if security hasn't been compromised.
             */
            if (isSet($_SESSION[$_field . $_ENC_SFX])) {

                if ($_SESSION[$_field] != $_text)
                    return $_ERROR;               // Field integrity compromised

            }

            return $_text;                        // Return decrypted value


        } else {

            return $_default;      // Field not defined, so return the default
        }

    }


    /**
     * stopOnWarnings - Set to stop script when warning messages are generated.
     *
     * @return bool  Returns TRUE meaning any warnings will stop the script.
     * @access public
     */
    function stopOnWarnings()
    {
        return $this->_stop_on_warn = TRUE;
    }


    /**
     * endStopOnWarnings - Set to keep script running when warning messages are
     * generated.
     *
     * @return bool  Returns FALSE meaning script will not stop on warnings.
     * @access public
     */
    function endStopOnWarnings()
    {
        return $this->_stop_on_warn = FALSE;
    }


    /**
     * warningsExist - A check to see if warning messages have been generated.
     *
     * @return bool  Returns TRUE if there are warning messages, otherwise FALSE
     * @access public
     */
    function warningsExist()
    {
        return (empty($this->_warnings)) ? FALSE : TRUE;
    }


    /**
     * flushWarnings - Clears all warning messages that may have been generated.
     *
     * @return string  Always returns NULL.
     * @access public
     */
    function flushWarnings()
    {
        return $this->_warnings = NULL;
    }


    /**
     * getWarnings - Retrieves and formats all warning messages for displaying.
     * Clears the warnings once called.
     *
     * @param  string $_color Font color to return warning in (HTML syntax).
     * @param  string $_size  Font size to return warning in (HTML syntax).
     * @return string Warning messages with HTML breaks/entities added.
     * @access public
     */
    function getWarnings($_color = 'BLUE', $_size = '+0')
    {
        if (empty($_color))
            $_color = 'BLUE';

        if (empty($_size))
            $_size  = '+0';

        $_warnMsgs = nl2br(htmlentities($this->_warnings, ENT_QUOTES));
        $_warnMsgs = $this->_formatFont($_warnMsgs, $_color, $_size);
        $this->flushWarnings();
        return $_warnMsgs;
    }


    /**
     * stopOnErrors - Set to stop script when error messages are generated.
     *
     * @return bool  Returns TRUE meaning any errors will stop the script.
     * @access public
     */
    function stopOnErrors()
    {
        return $this->_stop_on_error = TRUE;
    }


    /**
     * endStopOnErrors - Set to keep script running when error messages are
     * generated.
     *
     * @return bool  Returns FALSE meaning script will not stop on errors.
     * @access public
     */
    function endStopOnErrors()
    {
        return $this->_stop_on_error = FALSE;
    }


    /**
     * errorsExist - A check to see if error messages have been generated.
     *
     * @return bool  Returns TRUE if there are error messages, otherwise FALSE.
     * @access public
     */
    function errorsExist()
    {
        return (empty($this->_errors)) ? FALSE : TRUE;
    }


    /**
     * flushErrors - Clears all error messages that may have been generated.
     *
     * @return string  Always returns NULL.
     * @access public
     */
    function flushErrors()
    {
        return $this->_errors = NULL;
    }


    /**
     * getErrors - Retrieves and formats all error messages for displaying.
     * Clears the errors once called.
     *
     * @param  string $_color Font color to return error in (HTML syntax).
     * @param  string $_size  Font size to return error in (HTML syntax).
     * @return string Severe error messages with HTML breaks/entities added.
     * @access public
     */
    function getErrors($_color = 'RED', $_size = '+0')
    {
        if (empty($_color))
            $_color = 'RED';

        if (empty($_size))
            $_size  = '+0';

        $_errMsgs = nl2br(htmlentities($this->_errors, ENT_QUOTES));
        $_errMsgs = $this->_formatFont($_errMsgs, $_color, $_size);
        $this->flushErrors();
        return $_errMsgs;
    }


    /**
     * setSessURI - Appends the PHP session name and ID to the end of a URI.
     * It checks whether a question mark already is in the URI.
     * Useful for creating a URI to be used in a redirect (but less secure).
     *
     * @param  string $_uri A URI i.e. http://www.example.com/index.php
     * @return string The URI only, or URI with the session name and ID appended
     * @access public
     */
    function setSessURI($_uri)
    {

     	if (!empty($_uri)) {

            $_sess_id = session_id();

            if (!empty($_sess_id)) {   // instead of using SID
                if (FALSE === strstr($_uri, '?'))
                    $_uri .= '?' . $this->_sess_name . '=' . $_sess_id;
                else
                    $_uri .= $this->_ARG_SEP . $this->_sess_name . '=' .
                             $_sess_id;
            }

     	}

   	    return $_uri;
    }


    /**
     * createLink - Creates a link and appends the PHP session name and ID when
     * requested by setting $_add_sess to TRUE, which is the default.
     *
     * @param  string $_uri The URI for the link. i.e. http://www.example.com
     * @param  string $_desc The text description for the link. URI used if none
     * @param  string $_target Where to display upon click. i.e. _blank
     * @param  bool   $_add_sess When TRUE it adds session name and ID to link.
     * @return string HTML link or empty string.
     * @access public
     */
    function createLink($_uri,
                        $_desc     = NULL,
                        $_target   = NULL,
                        $_add_sess = TRUE
                       )
    {

     	if (empty($_uri))
  	        return '';

        if (!is_bool($_add_sess))
            $_add_sess = TRUE;

        $_desc = empty($_desc) ? $_uri : $_desc;

        if ($_add_sess)
            $_uri = $this->setSessURI($_uri);

     	if (empty($_target))
     	    return sprintf("<a href=\"%s\">%s</a>", $_uri, $_desc);
        else
     	    return sprintf("<a href=\"%s\" target=\"%s\">%s</a>",
     	                   $_uri,
     	                   $_target,
     	                   $_desc);

    }


    /**
     * getIPAddr - Detects and retrieves the IP address. If the value is
     * obtained from HTTP_X_FORWARDED_FOR, it could have multiple IP addresses.
     *
     * @param  string $type_used Passed by reference; used to return back a code
     * @return string Returns the IP address.
     * @return string Returns by reference a code used to signify the field type
     *                used to determine IP. Either: C, F, R, or U
     * @access public
     */
    function getIPAddr(&$type_used)
    {
        if (isSet($_SERVER['HTTP_CLIENT_IP'])) {
            $_ip = $_SERVER['HTTP_CLIENT_IP'];
            $type_used = 'C';

        } else
            if (isSet($_SERVER['HTTP_X_FORWARDED_FOR'])) {

                $_ip = $_SERVER['HTTP_X_FORWARDED_FOR'];
                $type_used = 'F';

       } else
            if (isSet($_SERVER['REMOTE_ADDR'])) {

                $_ip = $_SERVER['REMOTE_ADDR'];
                $type_used = 'R';

        } else {

                $_ip = 'UNKNOWN';
                $type_used = 'U';

        }

        return $_ip;
    }


    /**
     * secureConnection - Determines whether current connection is secure (SSL).
     *
     * @return bool Returns TRUE when this web connection is using SSL (HTTPS).
     * @access public
     */
    function secureConnection()
    {

        if (isSet($_SERVER['HTTPS']))
            return (0 === strcmp($_SERVER['HTTPS'], 'on')) ? TRUE : FALSE;
        else
            return FALSE;

    }


   /**
     * getVersion - Indicates the version number of this DB_eSession class.
     *
     * @return string Returns the current version number of this script.
     * @access public
     */
    function getVersion()
    {
        return $this->_ver;
    }


    /**
     * getSiteWarn - Formats a site warning message for displaying on your site.
     * When $_add_link is TRUE and warning message contains 'DB_eSession', it
     * will convert that text to a link to the author's web site.
     *
     * @param  string $_color Font color to return message in (HTML syntax).
     * @param  string $_size  Font size to return message in (HTML syntax).
     * @param  bool   $_center TRUE-centers message (adds <center></center>).
     * @param  bool   $_add_link When TRUE it creates a link to authors site.
     * @return string Returns the site warning message.
     * @access public
     */
    function getSiteWarn($_color = "NAVY", $_size = '-2', $_center = FALSE,
                         $_add_link = TRUE)
    {
        $_tmp_hold = $this->_warnings;
        $this->flushWarnings();
        $this->_setWrnMsg('SITE_WARN');
        $_msg = $this->_warnings;
        $this->_warnings = $_tmp_hold;

        $_msg = nl2br(htmlentities($_msg, ENT_QUOTES));

        if (empty($_color))
            $_color = 'NAVY';

        if (empty($_size))
            $_size  = '-2';

        if (!is_bool($_center))
            $_center = FALSE;

        if (!is_bool($_add_link))
            $_add_link = TRUE;

        if ($_add_link) {
            $_msg = str_replace('DB_eSession',
                           $this->createLink('http://www.code.dearneighbor.com',
                                             'DB_eSession', '_blank', FALSE),
                                $_msg);
        }

        $_msg = $this->_formatFont($_msg, $_color, $_size);

        if ($_center)
            $_msg = "<CENTER>{$_msg}</CENTER>";

        return $_msg;
    }


}   // End of DB_eSession class

// Make sure there are no whitespaces after the '>' character on the last line.
?>
