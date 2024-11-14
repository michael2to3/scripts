#!/bin/bash

#author         : Raul Calvo Laorden (me@r4ulcl.com)
#description    : Script to get WPA-EAP Identities, EAP certs, HTTP passwords, Handshakes, DNS queries, NBTNS queries and LLMNR queries
#date           : 2021-06-24
#usage          : bash pcapFilter.sh -f <pcap/folder> [options]
#-----------------------------------------------------------------------------------------------------------

red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`
#echo "${red}red text ${green}green text${reset}"


help () {
	echo "$0 -f <pcap/folder> [OPTION]

	-f <.pcap>: Read pcap or file of .caps
	-h : help

	OPTIONS:
		-A : all
		-P : Get HTTP POST passwords (HTTP)
		-I : Filter WPA-EAP Identity
		-C : Export EAP certs
		-H : Get Handshakes 1 and 2
		-D : Get DNS querys
		-R : Responder vulnerable protocols (NBT-NS + LLMNR)
		-N : Get NBT-NS querys
		-L : Get LLMNR querys
	"

}

filter () {

	echo -e "\n${green}FILE: $FILE${reset}"

	if [ ! -z "$ALL" ] ; then
		PASSWORDS=true
		IDENTITY=true
		HANDSHAKES=true
		DNS=true
		NBTNS=true
		LLMNR=true
		CERT=true
	fi

	if [ ! -z "$PASSWORDS" ] ; then
		echo -e "\n\tGet POST passwords\n"
		tshark -r $FILE -Y 'http.request.method == POST and (lower(http.file_data) contains "pass" or lower(http.request.line) contains "pass" or tcp contains "login")' -T fields -e http.file_data -e http.request.full_uri
		# basic auth?
	fi

	if [ ! -z "$IDENTITY" ] ; then
		echo -e "\n\tGet WPA-EAP Identities\n"
		echo -e 'DESTINATION\t\tSOURCE\t\t\tIDENTITY'
		tshark -nr $FILE -Y "eap.type == 1  && eap.code == 2" -T fields -e wlan.da -e wlan.sa -e eap.identity 2> /tmp/error | sort -u
		cat /tmp/error
	fi

	if [ ! -z "$HANDSHAKES" ] ; then
		echo -e "\n\tGet Handshakes in pcap\n"
		tshark -nr $FILE -Y "wlan_rsna_eapol.keydes.msgnr == 1 or wlan_rsna_eapol.keydes.msgnr == 2"
	fi

	if [ ! -z "$DNS" ] ; then
		echo -e "\n\tGet DNS querys\n"
		tshark -nr $FILE -Y "dns.flags == 0x0100" -T fields -e ip.src -e dns.qry.name
	fi

	if [ ! -z "$NBTNS" ] ; then
		echo -e "\n\tGet NBTNS querys in file to responder\n"
		tshark -nr $FILE -Y "nbns" -T fields -e ip.src -e nbns.name
	fi

	if [ ! -z "$LLMNR" ] ; then
		echo -e "\n\tGet LLMNR querys in file to responder\n"
		tshark -nr $FILE -Y "llmnr" -T fields -e ip.src -e dns.qry.name
	fi

	# https://gist.github.com/Cablethief/a2b8f0f7d5ece96423ba376d261bd711
	if [ ! -z "$CERT" ] ; then
		tmpbase=$(basename  $FILE)
		mkdir /tmp/certs/

		tshark -r $FILE \
		           -Y "ssl.handshake.certificate and eapol" \
		           -T fields -e "tls.handshake.certificate" -e "wlan.sa" -e "wlan.da" | while IFS= read -r line; do
			CERT=`echo $line | awk '{print $1}'`
			SA=`echo $line | awk '{print $2}'`
			DA=`echo $line | awk '{print $3}'`

			FILETMP=$(mktemp $tmpbase-$SA-$DA.cert.XXXX.der)

			echo -e "\n\n${green}Certificate from $SA to $DA ${reset}"
			echo -e "${green}Saved certificate in the file /tmp/certs/$FILETMP ${reset}"

			echo $CERT | \
			sed "s/://g" | \
			xxd -ps -r | \
			tee /tmp/certs/$FILETMP | \
			openssl x509 -inform der -text;

			rm $FILETMP
		done

		echo -e "\n\n${green}All certs saved in the /tmp/certs/ directory${reset}"

	fi
}

if [ ! -x $(which tshark) ]; then
  echo "${red}tshark not installed${reset}"
  exit 0
fi

while getopts hf:APIHDRNLC flag
do
    case "${flag}" in
        h) HELP=true;;
        f) INPUT=${OPTARG};;
        A) ALL=true;;
        P) PASSWORDS=true;;
        I) IDENTITY=true;;
        H) HANDSHAKES=true;;
        D) DNS=true;;
        R) NBTNS=true;LLMNR=true;;
        N) NBTNS=true;;
        L) LLMNR=true;;
	C) CERT=true;;
    esac
done

if [ "$HELP" = true ] ;
then
	help
	exit 0
fi

if [ -z "$INPUT" ] ; then
	echo "File or folder needed"
	echo
	help
	exit 1
fi


if [ -z "$ALL" ] && [ -z "$PASSWORDS" ] && [ -z "$IDENTITY" ] && [ -z "$HANDSHAKES" ] && [ -z "$DNS" ] && [ -z "$NBTNS" ] && [ -z "$LLMNR" ] && [ -z "$CERT" ]; then
	echo "Argument needed"
	help
	exit 2
fi

if [ "$#" -lt 3 ]; then
        echo "Argument needed"
        help
        exit 2
fi

#Check if INPUT is a folder
if [[ -d "$INPUT" ]]
then
	for F in $INPUT/*cap ; do
		if [ -f "$F" ] ; then
			FILE=$F
			filter
		else
			echo "${red}Warning: Some problem with \"$F\"${reset}"
		fi
	done
else
	FILE=$INPUT
	filter
fi


# # TODO
#- Passwords: basic auth, FTP, TFTP, SMB, SMB2, SMTP, POP3, IMAP
