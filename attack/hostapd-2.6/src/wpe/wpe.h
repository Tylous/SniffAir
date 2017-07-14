/*
    wpe.h - 
        brad.antoniewicz@foundstone.com
        Implements WPE (Wireless Pwnage Edition) functionality within 
        hostapd.

        WPE functionality focuses on targeting connecting users. At 
        it's core it implements credential logging (originally 
        implemented in FreeRADIUS-WPE), but also includes other patches
        for other client attacks.

            FreeRADIUS-WPE: https://github.com/brad-anton/freeradius-wpe
            Karma patch: http://foofus.net/goons/jmk/tools/hostapd-1.0-karma.diff
            Cupid patch: https://github.com/lgrangeia/cupid/blob/master/patch-hostapd
*/
#include <openssl/ssl.h>

struct wpe_config {
    char *wpe_logfile;
    FILE *wpe_logfile_fp;
    unsigned int wpe_enable_karma;
    unsigned int wpe_enable_cupid;
    unsigned int wpe_enable_return_success;
    unsigned int wpe_hb_send_before_handshake:1;
    unsigned int wpe_hb_send_before_appdata:1;
    unsigned int wpe_hb_send_after_appdata:1;
    unsigned int wpe_hb_payload_size;
    unsigned int wpe_hb_num_tries;
    unsigned int wpe_hb_num_repeats;
};

extern struct wpe_config wpe_conf;

extern char wpe_hb_msg[];
extern size_t wpe_hb_msg_len;

//#define WPE_HB_MSG_LEN 8

#define n2s(c,s)((s=(((unsigned int)(c[0]))<< 8)| \
       (((unsigned int)(c[1]))    )),c+=2)

#define s2n(s,c) ((c[0]=(unsigned char)(((s)>> 8)&0xff), \
        c[1]=(unsigned char)(((s)    )&0xff)),c+=2)


void wpe_log_file_and_stdout(char const *fmt, ...);
void wpe_log_chalresp(char *type, const u8 *username, size_t username_len, const u8 *challenge, size_t challenge_len, const u8 *response, size_t response_len);
void wpe_log_basic(char *type, const u8 *username, size_t username_len, const u8 *password, size_t password_len);
void wpe_hb_cb(int v_write_p, int v_version, int v_content_type, const void* v_buf, size_t v_len, SSL* v_ssl, void* v_arg);
char *wpe_hb_clear();
