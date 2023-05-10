interface=$(ip route get 8.8.8.8 | cut -d ' ' -f 5 | head -n 1)
ufw enable
sudo iptables -I INPUT -j ACCEPT
sudo iptables -I OUTPUT -o $interface -d 0.0.0.0/0 -j ACCEPT
sudo iptables -I INPUT -i $interface -m state --state ESTABLISHED,RELATED -j ACCEPT
sudo iptables -t mangle -A POSTROUTING -p tcp --tcp-flags SYN,RST SYN -o $interface -j TCPMSS --set-mss 1280
echo "done! please test your vpn connection"