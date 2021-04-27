import re
m = re.search(r'<g.*"translate\((\d+),(\d+)\)".*\n<rect.*width="(\d+)".*\n.*<text id="{}-{}"[\d\D]*?</g>'
                            .format(re.escape("A9178943"),re.escape("A6B967DF23BB"))
              , """
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1"  width="3472" height="2212">
<defs id="dmw_defs" >
<svg id="fk_sym" viewBox="0 0 48.665 48.665" style="enable-background:new 0 0 48.665 48.665;" >
<g>
<path d="M40.332,31.592c-2.377,0-4.515,1-6.033,2.598l-17.737-8.686c0.061-0.406,0.103-0.82,0.103-1.246    c0-0.414-0.04-0.818-0.098-1.215l17.711-8.589c1.519,1.609,3.666,2.619,6.054,2.619c4.603,0,8.333-3.731,8.333-8.333    c0-4.603-3.73-8.333-8.333-8.333s-8.333,3.73-8.333,8.333c0,0.414,0.04,0.817,0.098,1.215l-17.709,8.589    c-1.519-1.609-3.666-2.619-6.054-2.619C3.73,15.925,0,19.656,0,24.258c0,4.603,3.73,8.333,8.333,8.333    c2.377,0,4.515-1,6.033-2.596l17.736,8.685c-0.062,0.406-0.104,0.82-0.104,1.245c0,4.604,3.73,8.333,8.333,8.333    s8.333-3.729,8.333-8.333C48.665,35.322,44.935,31.592,40.332,31.592z" fill="#13bf3b"/>
</g>
</svg>
<svg id="pk_sym" viewBox="0 0 480.509 480.509" style="enable-background:new 0 0 480.509 480.509;" >
<g>
<path d="M418.119,331.046c4.094,4.374,7.766,8.186,10.996,11.416c3.237,3.238,6.714,6.376,10.427,9.422   c3.71,3.042,6.427,4.568,8.135,4.568c3.241,0,9.517-4.661,18.843-13.99c9.328-9.321,13.989-15.604,13.989-18.842   c0-1.523-2.714-5.421-8.138-11.704c-5.421-6.276-12.364-13.702-20.838-22.271c-8.473-8.565-16.703-16.744-24.694-24.55   c-8.001-7.81-15.8-15.373-23.417-22.703c-7.611-7.327-11.992-11.56-13.135-12.703c-1.902-1.902-4.093-2.853-6.563-2.853   c-3.237,0-9.521,4.661-18.843,13.988c-9.328,9.322-13.989,15.605-13.989,18.843c0,1.711,1.522,4.421,4.568,8.138   c3.046,3.71,6.188,7.187,9.421,10.424c3.23,3.23,7.047,6.899,11.42,10.992c4.377,4.093,6.848,6.423,7.423,6.995l-27.408,27.404   L254.954,222.268c24.94-33.498,37.408-68.236,37.408-104.211c0-31.024-9.761-56.293-29.263-75.801   c-19.512-19.511-44.778-29.265-75.805-29.265c-30.454,0-60.244,9.042-89.363,27.119c-29.121,18.083-52.727,41.686-70.808,70.808   C9.042,140.038,0,169.828,0,200.28c0,31.029,9.753,56.286,29.265,75.803c19.511,19.517,44.777,29.27,75.801,29.27   c35.976,0,70.71-12.467,104.212-37.407l191.574,191.579c5.332,5.328,11.796,7.994,19.417,7.994c7.991,0,15.704-3.72,23.12-11.14   c7.426-7.426,11.143-15.129,11.143-23.127c0-7.617-2.666-14.092-7.994-19.417l-62.811-62.811l27.405-27.404   C411.699,324.195,414.033,326.666,418.119,331.046z M221.556,161.458c-10.656,10.657-23.601,15.987-38.828,15.987   c-7.996,0-15.896-1.812-23.7-5.43c3.617,7.808,5.426,15.706,5.426,23.7c0,15.229-5.327,28.171-15.987,38.828   c-10.66,10.655-23.606,15.986-38.831,15.986c-15.227,0-28.168-5.325-38.828-15.986c-10.657-10.657-15.987-23.599-15.987-38.828   c0-15.227,5.327-28.171,15.987-38.828C81.464,146.23,94.409,140.9,109.636,140.9c7.992,0,15.893,1.809,23.695,5.424   c-3.616-7.804-5.424-15.706-5.424-23.699c0-15.227,5.327-28.171,15.987-38.828c10.66-10.657,23.604-15.987,38.831-15.987   c15.227,0,28.171,5.327,38.828,15.987c10.657,10.66,15.987,23.601,15.987,38.828C237.539,137.852,232.209,150.797,221.556,161.458z   " fill="#ff8345"/>
</g>
</svg>
<svg id="uk_sym" viewBox="0 0 490 490" style="enable-background:new 0 0 490 490;" >
<g>
	<polygon points="236.99,11.41 0,246.348 236.99,478.678 236.99,350.609 129.864,245 236.99,139.391  " fill="#0064fb"/>
<polygon points="253.01,478.59 490,243.651 253.01,11.322 253.01,139.391 360.136,245 253.01,350.609  " fill="#0064fb"/>
</g>
</svg>
<svg id="link_sym" viewBox="0 0 1000 900" style="enable-background:new 0 0 1000 900;" >
<g>
<path fill="black" d="M660.224 422.656c6.976 16.192-0.512 35.008-16.768 42.048-16.128 6.976-34.944-0.448-41.984-16.768-8.448-19.776-20.736-37.696-36.224-53.248-64.64-64.64-177.344-64.64-241.92 0l-145.216 145.28c-66.688 66.688-66.688 175.232 0 241.984 66.688 66.688 175.104 66.752 241.92 0l92.8-92.864c12.48-12.48 32.768-12.48 45.248 0s12.48 32.768 0 45.248l-92.8 92.864c-91.648 91.648-240.832 91.52-332.416 0-91.712-91.648-91.712-240.832 0-332.48l145.216-145.28c44.352-44.416 103.424-68.864 166.272-68.864s121.792 24.448 166.208 68.864c21.248 21.312 38.016 45.952 49.664 73.216zM891.136 401.344l-145.216 145.216c-88.768 88.832-243.712 88.832-332.416 0-21.312-21.312-38.080-45.952-49.728-73.216-7.040-16.256 0.448-35.072 16.704-42.048 16.064-6.784 35.008 0.512 41.984 16.768 8.512 19.776 20.8 37.696 36.288 53.248 64.64 64.64 177.344 64.64 241.92 0l145.216-145.216c66.688-66.688 66.688-175.232 0-241.984-66.752-66.624-175.168-66.688-241.92 0l-92.8 92.864c-12.48 12.48-32.768 12.48-45.248 0s-12.48-32.768 0-45.248l92.8-92.864c45.824-45.824 105.984-68.736 166.208-68.736s120.448 22.912 166.272 68.736c91.584 91.648 91.584 240.768-0.064 332.48z" />
</g>
</svg>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath31_0_">
<rect x="0" y="0" width="111" height="60" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath38_0_">
<rect x="0" y="0" width="170" height="110" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath39_0_">
<rect x="0" y="0" width="170" height="110" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath21_0_">
<rect x="0" y="0" width="160" height="79" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath35_0_">
<rect x="0" y="0" width="170" height="110" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath41_0_">
<rect x="0" y="0" width="111" height="30" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath25_0_">
<rect x="0" y="0" width="73" height="27" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath28_0_">
<rect x="0" y="0" width="137" height="64" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath15_0_">
<rect x="0" y="0" width="111" height="28" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath18_0_">
<rect x="0" y="0" width="132" height="84" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath11_0_">
<rect x="0" y="0" width="283" height="162" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath10_0_">
<rect x="0" y="0" width="358" height="371" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath36_0_">
<rect x="0" y="0" width="170" height="110" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath42_0_">
<rect x="0" y="0" width="131" height="68" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath20_0_">
<rect x="0" y="0" width="147" height="81" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath27_0_">
<rect x="0" y="0" width="129" height="79" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath33_0_">
<rect x="0" y="0" width="170" height="114" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath8_0_">
<rect x="0" y="0" width="153" height="27" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath24_0_">
<rect x="0" y="0" width="70" height="27" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath6_0_">
<rect x="0" y="0" width="111" height="60" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath9_0_">
<rect x="0" y="0" width="191" height="135" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath3_0_">
<rect x="0" y="0" width="111" height="27" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath37_0_">
<rect x="0" y="0" width="170" height="110" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath32_0_">
<rect x="0" y="0" width="161" height="27" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath45_0_">
<rect x="0" y="0" width="341" height="266" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath13_0_">
<rect x="0" y="0" width="111" height="28" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath7_0_">
<rect x="0" y="0" width="111" height="28" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath30_0_">
<rect x="0" y="0" width="161" height="27" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath46_0_">
<rect x="0" y="0" width="111" height="74" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath1_0_">
<rect x="0" y="0" width="143" height="53" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath12_0_">
<rect x="0" y="0" width="271" height="194" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath23_0_">
<rect x="0" y="0" width="119" height="27" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath44_0_">
<rect x="0" y="0" width="126" height="51" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath29_0_">
<rect x="0" y="0" width="143" height="53" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath26_0_">
<rect x="0" y="0" width="137" height="64" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath19_0_">
<rect x="0" y="0" width="72" height="27" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath17_0_">
<rect x="0" y="0" width="192" height="96" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath2_0_">
<rect x="0" y="0" width="150" height="101" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath22_0_">
<rect x="0" y="0" width="113" height="53" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath34_0_">
<rect x="0" y="0" width="170" height="113" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath43_0_">
<rect x="0" y="0" width="181" height="101" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath5_0_">
<rect x="0" y="0" width="111" height="60" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath40_0_">
<rect x="0" y="0" width="170" height="110" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath16_0_">
<rect x="0" y="0" width="111" height="30" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath14_0_">
<rect x="0" y="0" width="137" height="64" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath4_0_">
<rect x="0" y="0" width="147" height="77" />
</clipPath>
</defs>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-dasharray="8,8" stroke-width="1" d="M2946 1218 L2946 1278" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2946 1218 2949 1224 2943 1224" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2940.0 1272.0 L2952.0 1272.0 M2940.0 1266.6000003814697 L2952.0 1266.6000003814697" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-dasharray="8,8" stroke-width="1" d="M1214 944 L1264 944 L1264 1050 L1135 1050 L1135 1000" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1214 944 1220 941 1220 947" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1141.0 1000.0 L1135.0 1012.0 L1129.0 1000.0 M1141.0 1012.5999994277954 L1129.0 1012.5999994277954" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M402 1985 L143 985" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="402 1985 399 1980 403 1980" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M149.0 989.0 L139.0 991.0 M149.89999997615814 993.5 L139.89999997615814 995.5" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M739 1444 L3191 933" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="739 1444 744 1441 744 1445" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M3192.0 938.0 L3181.0 935.0 L3190.0 928.0 M3181.5 940.0999999046326 L3179.5 930.0999999046326" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M3257 961 L2791 1715" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="3257 961 3256 967 3252 965" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2786.0 1712.0 L2797.0 1705.0 L2796.0 1718.0 M2792.2999997138977 1701.5 L2802.2999997138977 1707.5" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M2891 1282 L2285 1012" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2891 1282 2885 1282 2887 1278" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2292.0 1009.0 L2288.0 1019.0 M2296.5 1010.7999999523163 L2292.5 1020.7999999523163" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-dasharray="8,8" stroke-width="1" d="M2052 967 L2435 1302" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2052 967 2057 968 2055 972" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2428.0 1303.0 L2434.0 1295.0 M2424.4000000953674 1300.3000001907349 L2430.4000000953674 1292.3000001907349" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1400 1152 L1400 1114" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1400 1152 1397 1146 1403 1146" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1406.0 1114.0 L1400.0 1126.0 L1394.0 1114.0 M1406.0 1126.5999994277954 L1394.0 1126.5999994277954" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1391 655 L1129 1060" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1391 655 1390 661 1386 659" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1124.0 1057.0 L1135.0 1050.0 L1134.0 1063.0 M1130.2999997138977 1046.5 L1140.2999997138977 1052.5" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M2163 1830 L2163 1301" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2163 1830 2160 1824 2166 1824" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2169.0 1301.0 L2163.0 1313.0 L2157.0 1301.0 M2169.0 1313.5999994277954 L2157.0 1313.5999994277954" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M3347 961 L3347 1021" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="3347 961 3350 967 3344 967" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M3341.0 1015.0 L3353.0 1015.0 M3341.0 1009.6000003814697 L3353.0 1009.6000003814697" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M2940 1131 L2940 1191" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2940 1131 2943 1137 2937 1137" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2934.0 1185.0 L2946.0 1185.0 M2934.0 1179.6000003814697 L2946.0 1179.6000003814697" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M989 1658 L1078 1658" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="989 1658 995 1655 995 1661" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1078.0 1664.0 L1066.0 1658.0 L1078.0 1652.0 M1065.4000005722046 1664.0 L1065.4000005722046 1652.0" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M2649 916 L2087 916" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2649 916 2643 919 2643 913" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2087.0 910.0 L2099.0 916.0 L2087.0 922.0 M2099.5999994277954 910.0 L2099.5999994277954 922.0" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M739 1426 L1379 1213" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="739 1426 744 1423 744 1427" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1380.0 1218.0 L1369.0 1215.0 L1378.0 1208.0 M1369.5 1220.0999999046326 L1367.5 1210.0999999046326" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M2604 1242 L2604 1302" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2604 1242 2607 1248 2601 1248" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2598.0 1302.0 L2604.0 1290.0 L2610.0 1302.0 M2598.0 1289.4000005722046 L2610.0 1289.4000005722046" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-dasharray="8,8" stroke-width="1" d="M2509 1349 L2700 1410" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2509 1349 2514 1348 2514 1352" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2699.0 1415.0 L2690.0 1408.0 L2701.0 1405.0 M2688.5 1412.9000000953674 L2690.5 1402.9000000953674" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M2074 967 L2074 1352" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2074 967 2077 973 2071 973" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2068.0 1346.0 L2080.0 1346.0 M2068.0 1340.6000003814697 L2080.0 1340.6000003814697" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M2087 943 L2235 987" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2087 943 2092 942 2092 946" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2229.0 991.0 L2231.0 981.0 M2224.5 990.1000000238419 L2226.5 980.1000000238419" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M878 1637 L190 985" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="878 1637 872 1635 876 1631" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M194.0 981.0 L198.0 993.0 L186.0 989.0 M202.39999961853027 989.3999996185303 L194.39999961853027 997.3999996185303" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1094 752 L1094 692" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1094 752 1091 746 1097 746" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1100.0 692.0 L1094.0 704.0 L1088.0 692.0 M1100.0 704.5999994277954 L1088.0 704.5999994277954" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-dasharray="8,8" stroke-width="1" d="M720 367 L770 367 L770 444 L663 444 L663 394" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="720 367 726 364 726 370" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M669.0 394.0 L663.0 406.0 L657.0 394.0 M669.0 406.5999994277954 L657.0 406.5999994277954" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M726 1555 L857 1637" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="726 1555 732 1556 730 1560" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M854.0 1642.0 L847.0 1631.0 L860.0 1632.0 M843.5 1635.7000002861023 L849.5 1625.7000002861023" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1354 655 L1175 865" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1354 655 1353 660 1349 658" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1174.0 858.0 L1182.0 864.0 M1176.6999998092651 854.4000000953674 L1184.6999998092651 860.4000000953674" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1104 1060 L1104 1000" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1104 1060 1101 1054 1107 1054" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1110.0 1000.0 L1104.0 1012.0 L1098.0 1000.0 M1110.0 1012.5999994277954 L1098.0 1012.5999994277954" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-dasharray="8,8" stroke-width="1" d="M2497 1654 L2179 1845" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2497 1654 2493 1659 2491 1655" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2176.0 1840.0 L2189.0 1839.0 L2182.0 1850.0 M2186.5 1833.7000002861023 L2192.5 1843.7000002861023" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1406 655 L1095 1199" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1406 655 1406 661 1402 659" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1090.0 1197.0 L1099.0 1189.0 L1100.0 1201.0 M1094.1999998092651 1186.5 L1104.1999998092651 1190.5" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M452 1985 L662 1788" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="452 1985 454 1979 458 1983" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M662.0 1796.0 L654.0 1788.0 M658.4000000953674 1799.5999999046326 L650.4000000953674 1791.5999999046326" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M989 1673 L1078 1673" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="989 1673 995 1670 995 1676" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1078.0 1679.0 L1066.0 1673.0 L1078.0 1667.0 M1065.4000005722046 1679.0 L1065.4000005722046 1667.0" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1379 1179 L223 960" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1379 1179 1374 1180 1374 1176" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M224.0 955.0 L233.0 962.0 L222.0 965.0 M234.5 957.0999999046326 L232.5 967.0999999046326" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M88 637 L88 577" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="88 637 85 631 91 631" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M94.0 577.0 L88.0 589.0 L82.0 577.0 M94.0 589.5999994277954 L82.0 589.5999994277954" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M739 1443 L2649 1034" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="739 1443 744 1440 744 1444" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2650.0 1039.0 L2639.0 1036.0 L2648.0 1029.0 M2639.5 1041.0999999046326 L2637.5 1031.0999999046326" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M2649 1070 L2318 1210" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2649 1070 2645 1074 2643 1070" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2316.0 1205.0 L2328.0 1206.0 L2320.0 1215.0 M2326.5 1200.8000001907349 L2330.5 1210.8000001907349" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M471 1555 L471 1985" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="471 1555 474 1561 468 1561" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M465.0 1979.0 L477.0 1979.0 M465.0 1973.6000003814697 L477.0 1973.6000003814697" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-dasharray="8,8" stroke-width="1" d="M2300 1012 L2906 1278" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2300 1012 2306 1012 2304 1016" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2899.0 1281.0 L2903.0 1271.0 M2894.5 1279.2000000476837 L2898.5 1269.2000000476837" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-dasharray="8,8" stroke-width="1" d="M2538 1242 L2113 1830" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2538 1242 2537 1247 2533 1245" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2109.0 1827.0 L2119.0 1822.0 L2117.0 1833.0 M2115.2999997138977 1818.6000003814697 L2123.2999997138977 1824.6000003814697" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1906 898 L635 645" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1906 898 1901 899 1901 895" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M636.0 640.0 L645.0 647.0 L634.0 650.0 M646.5 642.0999999046326 L644.5 652.0999999046326" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M198 908 L480 684" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="198 908 201 903 203 907" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M483.0 688.0 L472.0 690.0 L477.0 680.0 M474.6000003814697 694.2999997138977 L468.6000003814697 686.2999997138977" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1080 1199 L1080 1139" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1080 1199 1077 1193 1083 1193" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1086.0 1139.0 L1080.0 1151.0 L1074.0 1139.0 M1086.0 1151.5999994277954 L1074.0 1151.5999994277954" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M857 1720 L747 1720" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="857 1720 851 1723 851 1717" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M747.0 1714.0 L759.0 1720.0 L747.0 1726.0 M759.5999994277954 1714.0 L759.5999994277954 1726.0" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M647 1788 L392 1985" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="647 1788 644 1793 642 1789" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M393.0 1978.0 L399.0 1986.0 M396.59999990463257 1975.3000001907349 L402.59999990463257 1983.3000001907349" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M432 1985 L1072 692" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="432 1985 432 1979 436 1981" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1077.0 694.0 L1068.0 702.0 L1067.0 690.0 M1072.8000001907349 704.5 L1062.8000001907349 700.5" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1908 1839 L1723 1720" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1908 1839 1902 1838 1904 1834" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1731.0 1718.0 L1725.0 1728.0 M1735.5 1720.6999998092651 L1729.5 1730.6999998092651" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1023 992 L914 1060" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1023 992 1019 997 1017 993" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M916.0 1052.0 L922.0 1062.0 M920.5 1049.3000001907349 L926.5 1059.3000001907349" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M2602 1658 L2680 1715" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2602 1658 2607 1659 2605 1663" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2677.0 1719.0 L2672.0 1709.0 L2683.0 1711.0 M2668.6000003814697 1712.7000002861023 L2674.6000003814697 1704.7000002861023" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1908 1870 L1544 1720" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1908 1870 1902 1870 1904 1866" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1551.0 1717.0 L1547.0 1727.0 M1555.5 1718.7999999523163 L1551.5 1728.7999999523163" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1679 655 L1679 1327" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1679 655 1682 661 1676 661" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1673.0 1327.0 L1679.0 1315.0 L1685.0 1327.0 M1673.0 1314.4000005722046 L1685.0 1314.4000005722046" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M133 908 L133 577" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="133 908 130 902 136 902" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M139.0 577.0 L133.0 589.0 L127.0 577.0 M139.0 589.5999994277954 L127.0 589.5999994277954" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M158 985 L447 1985" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="158 985 161 990 157 990" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M441.0 1981.0 L451.0 1979.0 M440.10000002384186 1976.5 L450.10000002384186 1974.5" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M2074 967 L2589 1302" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2074 967 2080 968 2078 972" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2586.0 1307.0 L2579.0 1296.0 L2592.0 1297.0 M2575.5 1300.7000002861023 L2581.5 1290.7000002861023" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1944 967 L1944 1352" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1944 967 1947 973 1941 973" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1938.0 1346.0 L1950.0 1346.0 M1938.0 1340.6000003814697 L1950.0 1340.6000003814697" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M3211 961 L3211 1021" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="3211 961 3214 967 3208 967" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M3205.0 1015.0 L3217.0 1015.0 M3205.0 1009.6000003814697 L3217.0 1009.6000003814697" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-dasharray="8,8" stroke-width="1" d="M1505 1068 L1505 1152" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1505 1068 1508 1074 1502 1074" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1499.0 1152.0 L1505.0 1140.0 L1511.0 1152.0 M1499.0 1139.4000005722046 L1511.0 1139.4000005722046" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1938 1830 L1938 1697" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1938 1830 1935 1824 1941 1824" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1944.0 1703.0 L1932.0 1703.0 M1944.0 1708.3999996185303 L1932.0 1708.3999996185303" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-dasharray="8,8" stroke-width="1" d="M2501 1242 L2501 1302" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2501 1242 2504 1248 2498 1248" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2495.0 1296.0 L2507.0 1296.0 M2495.0 1290.6000003814697 L2507.0 1290.6000003814697" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1991 1830 L1782 1437" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1991 1830 1987 1826 1991 1824" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1787.0 1435.0 L1786.0 1447.0 L1777.0 1439.0 M1791.1999998092651 1445.5 L1781.1999998092651 1449.5" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M456 1985 L456 1555" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="456 1985 453 1979 459 1979" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M462.0 1561.0 L450.0 1561.0 M462.0 1566.3999996185303 L450.0 1566.3999996185303" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M2420 1302 L2037 967" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2420 1302 2415 1301 2417 1297" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2044.0 966.0 L2038.0 974.0 M2047.5999999046326 968.6999998092651 L2041.5999999046326 976.6999998092651" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M914 1637 L658 394" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="914 1637 911 1632 915 1632" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M663.0 393.0 L660.0 404.0 L653.0 395.0 M665.0999999046326 403.5 L655.0999999046326 405.5" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M2659 1131 L2587 1191" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2659 1131 2656 1136 2654 1132" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2584.0 1187.0 L2595.0 1185.0 L2590.0 1195.0 M2592.3999996185303 1180.7000002861023 L2598.3999996185303 1188.7000002861023" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1094 865 L1094 805" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1094 865 1091 859 1097 859" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1100.0 805.0 L1094.0 817.0 L1088.0 805.0 M1100.0 817.5999994277954 L1088.0 817.5999994277954" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M2069 2024 L2069 2182" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2069 2024 2072 2030 2066 2030" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2063.0 2176.0 L2075.0 2176.0 M2063.0 2170.6000003814697 L2075.0 2170.6000003814697" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-dasharray="8,8" stroke-width="1" d="M2620 1231 L2891 1294" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2620 1231 2625 1230 2625 1234" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2885.0 1298.0 L2887.0 1288.0 M2880.5 1297.1000000238419 L2882.5 1287.1000000238419" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1921 2024 L1921 2182" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1921 2024 1924 2030 1918 2030" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1915.0 2176.0 L1927.0 2176.0 M1915.0 2170.6000003814697 L1927.0 2170.6000003814697" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1415 1152 L1415 1114" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1415 1152 1412 1146 1418 1146" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1421.0 1114.0 L1415.0 1126.0 L1409.0 1114.0 M1421.0 1126.5999994277954 L1409.0 1126.5999994277954" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M2990 1101 L3138 1191" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2990 1101 2996 1102 2994 1106" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M3130.0 1193.0 L3136.0 1183.0 M3125.5 1190.3000001907349 L3131.5 1180.3000001907349" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M739 1484 L2497 1616" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="739 1484 744 1482 744 1486" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2497.0 1621.0 L2487.0 1616.0 L2497.0 1611.0 M2486.5 1621.0 L2486.5 1611.0" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-dasharray="8,8" stroke-width="1" d="M2898 1338 L2803 1398" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2898 1338 2894 1343 2892 1339" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2800.0 1393.0 L2813.0 1392.0 L2806.0 1403.0 M2810.5 1386.7000002861023 L2816.5 1396.7000002861023" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1908 1885 L1365 1720" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1908 1885 1903 1886 1903 1882" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1371.0 1716.0 L1369.0 1726.0 M1375.5 1716.8999999761581 L1373.5 1726.8999999761581" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g  fill="rgb(255,255,180)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath39_0_)" transform="translate(465,574)" >
<rect x="0" y="0" width="169" height="109" />
<text id="0CCF19A2-A5AB6077BA49" x="54" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Relation_61
</text>
<line x1="0" y1="17" x2="168" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Ansprechpartner_Ansprechpartner_ID
</text>
<text x="342" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID
</text>
<text x="342" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="56" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebskunde_Vertriebskunde_ID
</text>
<text x="342" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="62" x2="168" y2="62" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="69" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="75" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_61_PK (Ansprechpartner_Ansprechpartner_ID, Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID, Vertriebskunde_Vertriebskunde_ID)
</text>
<line x1="0" y1="81" x2="168" y2="81" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="88" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#FA90040D-641F12C234A3" >
<text x="16" y="94" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_61_Ansprechpartner_FK (Ansprechpartner_Ansprechpartner_ID)
</text></a>
<use xlink:href="#fk_sym" x="4" y="101" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#E4C6AAFE-6B5E5EF62F40" >
<text x="16" y="107" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_61_Vertriebskunde_FK (Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID, Vertriebskunde_Vertriebskunde_ID)
</text></a>
</g>
<g  fill="rgb(255,255,180)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath38_0_)" transform="translate(1252,1004)" >
<rect x="0" y="0" width="169" height="109" />
<text id="090552D2-19B7D8DBC5E7" x="54" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Relation_57
</text>
<line x1="0" y1="17" x2="168" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
natürliche_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID
</text>
<text x="398" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
natürliche_Person_natürliche_Person_ID
</text>
<text x="398" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="56" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
natürliche_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID1
</text>
<text x="398" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="69" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="69" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
natürliche_Person_natürliche_Person_ID1
</text>
<text x="398" y="69" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="75" x2="168" y2="75" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="82" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="88" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_57_PK (natürliche_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID, natürliche_Person_natürliche_Person_ID, natürliche_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID1, natürliche_Person_natürliche_Person_ID1)
</text>
<line x1="0" y1="94" x2="168" y2="94" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="101" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#4E447132-09B3FE5665A4" >
<text x="16" y="107" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_57_natürliche_Person_FK (natürliche_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID, natürliche_Person_natürliche_Person_ID)
</text></a>
<use xlink:href="#fk_sym" x="4" y="114" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#4E447132-09B3FE5665A4" >
<text x="16" y="120" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_57_natürliche_Person_FKv1 (natürliche_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID1, natürliche_Person_natürliche_Person_ID1)
</text></a>
<polygon points="162,106 158,98 166,98" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(203,218,124)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath4_0_)" transform="translate(76,908)" >
<rect x="0" y="0" width="146" height="76" />
<text id="FA90040D-641F12C234A3" x="28" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Ansprechpartner
</text>
<line x1="0" y1="17" x2="145" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Gültigkeitsperiode
</text>
<text x="393" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Ansprechpartner_ID
</text>
<text x="393" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Juristische_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID
</text>
<text x="393" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="69" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
natürliche_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID
</text>
<text x="393" y="69" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="82" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="82" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="82" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
natürliche_Person_natürliche_Person_ID
</text>
<text x="393" y="82" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="139,73 135,65 143,65" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="88" x2="145" y2="88" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="95" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="101" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Ansprechpartner_PK (Ansprechpartner_ID)
</text>
<polygon points="139,73 135,65 143,65" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="107" x2="145" y2="107" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="114" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#3791AFE5-FA89BDDBAB70" >
<text x="16" y="120" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Ansprechpartner_Juristische_Person_FK (Juristische_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID)
</text></a>
<polygon points="139,73 135,65 143,65" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="126" x2="145" y2="126" fill="none" stroke="rgb(0,0,255)"/>
<text x="2" y="139" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
U
</text>
<text x="16" y="139" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Ansprechpartner__IDX (Kommunikationsmittel_Kommunikationsmittel_ID)
</text>
<polygon points="139,73 135,65 143,65" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(203,218,124)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath2_0_)" transform="translate(1022,591)" >
<rect x="0" y="0" width="149" height="100" />
<text id="D9B340FA-CCE6AE3FF6E1" x="53" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Adresse
</text>
<line x1="0" y1="17" x2="148" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Adresstyp
</text>
<text x="287" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Strassenname
</text>
<text x="287" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Hausnr
</text>
<text x="287" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="69" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Gebäudename
</text>
<text x="287" y="69" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="82" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="82" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Geokoordinate
</text>
<text x="287" y="82" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="95" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="95" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="95" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Adresse_ID
</text>
<text x="287" y="95" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="108" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="108" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
bild1_bild1_ID
</text>
<text x="287" y="108" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="142,97 138,89 146,89" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="114" x2="148" y2="114" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="121" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="127" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Adresse_PK (Adresse_ID)
</text>
<polygon points="142,97 138,89 146,89" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="133" x2="148" y2="133" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="140" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#C0B4ACF6-15D198ED9BD8" >
<text x="16" y="146" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Adresse_PLZ-Gebiet_FK (PLZ-Gebiet_Gebiet_Geografische_Einheit_GEIN_ID, PLZ-Gebiet_PLZ-Gebiet_ID)
</text></a>
<polygon points="142,97 138,89 146,89" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="152" x2="148" y2="152" fill="none" stroke="rgb(0,0,255)"/>
<text x="2" y="165" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
U
</text>
<text x="16" y="165" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Adresse__IDX (bild1_bild1_ID)
</text>
<polygon points="142,97 138,89 146,89" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath45_0_)" transform="translate(2649,865)" >
<rect x="0" y="0" width="340" height="265" />
<text id="92B0C5FC-140E14D85F0C" x="117" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Vertriebsteilnehmer
</text>
<line x1="0" y1="17" x2="339" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebsteilnehmer_ID
</text>
<text x="300" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID
</text>
<text x="300" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="49" x2="339" y2="49" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="56" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="62" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebsteilnehmer_PK (Vertriebsteilnehmer_ID)
</text>
<line x1="0" y1="68" x2="339" y2="68" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="75" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#38FC9743-5D02070CB9D4" >
<text x="16" y="81" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebsteilnehmer_Geschäftsfähige_Einheit_FK (Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID)
</text></a>
</g>
<g  fill="rgb(153,255,0)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath21_0_)" transform="translate(1024,1060)" >
<rect x="0" y="0" width="159" height="78" />
<text id="19B5F296-1D5FC327C71A" x="67" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Land
</text>
<line x1="0" y1="17" x2="158" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
U
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
ISO2_Code
</text>
<text x="262" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
VARCHAR2 (2 CHAR)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
ISO3_Code
</text>
<text x="262" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
VARCHAR2 (2 CHAR)
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
ISO_Code_numerisch
</text>
<text x="262" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
VARCHAR2 (2 CHAR)
</text>
<text x="16" y="69" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
TopLevelDomain
</text>
<text x="262" y="69" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="82" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="82" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="82" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
LAND_ID
</text>
<text x="262" y="82" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="152,75 148,67 156,67" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="88" x2="158" y2="88" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="95" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="101" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
LAND_PK (Geografische_Einheit_GEIN_ID, LAND_ID)
</text>
<polygon points="152,75 148,67 156,67" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="107" x2="158" y2="107" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="114" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#4623645A-68B64E30D79B" >
<text x="16" y="120" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Land_Geografische_Einheit_FK (Geografische_Einheit_GEIN_ID)
</text></a>
<polygon points="152,75 148,67 156,67" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(203,218,124)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath11_0_)" transform="translate(456,1393)" >
<rect x="0" y="0" width="282" height="161" />
<text id="38FC9743-5D02070CB9D4" x="79" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Geschäftsfähige_Einheit
</text>
<line x1="0" y1="17" x2="281" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Geschäftsfähige_Einheit_ID
</text>
<text x="288" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Name
</text>
<text x="288" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Kommunikationsmittel_Kommunikationsmittel_ID
</text>
<text x="288" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="62" x2="281" y2="62" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="69" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="75" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Geschäftsfähige_Einheit_PK (Geschäftsfähige_Einheit_ID)
</text>
<line x1="0" y1="81" x2="281" y2="81" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="88" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#4B8B3C74-CEEE2315D8E7" >
<text x="16" y="94" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Geschäftsfähige_Einheit_Kommunikationsmittel_FK (Kommunikationsmittel_Kommunikationsmittel_ID)
</text></a>
<line x1="0" y1="100" x2="281" y2="100" fill="none" stroke="rgb(0,0,255)"/>
<text x="2" y="113" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
U
</text>
<text x="16" y="113" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Geschäftsfähige_Einheit__IDX (Kommunikationsmittel_Kommunikationsmittel_ID)
</text>
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath32_0_)" transform="translate(3311,1021)" >
<rect x="0" y="0" width="160" height="26" />
<text id="8D70D427-FAE524E0B003" x="20" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Qualifizierter_Interessent
</text>
<line x1="0" y1="17" x2="159" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Interessent_Interessent_ID
</text>
<text x="187" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="153,23 149,15 157,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="36" x2="159" y2="36" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="43" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="49" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Qualifizierter_Interessent_PK (Interessent_Interessent_ID)
</text>
<polygon points="153,23 149,15 157,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="55" x2="159" y2="55" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="62" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#C5F5C08D-A2771073ED98" >
<text x="16" y="68" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Qualifizierter_Interessent_Interessent_FK (Interessent_Interessent_ID)
</text></a>
<polygon points="153,23 149,15 157,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath43_0_)" transform="translate(1906,866)" >
<rect x="0" y="0" width="180" height="100" />
<text id="E4C6AAFE-6B5E5EF62F40" x="49" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Vertriebskunde
</text>
<line x1="0" y1="17" x2="179" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebskunde_ID
</text>
<text x="262" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebsteilnehmer_Vertriebsteilnehmer_ID
</text>
<text x="262" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Besitzer_Besitzer_ID
</text>
<text x="262" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="62" x2="179" y2="62" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="69" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="75" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebskunde_PK (Vertriebsteilnehmer_Vertriebsteilnehmer_ID, Vertriebskunde_ID)
</text>
<use xlink:href="#uk_sym" x="4" y="82" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="88" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebskunde_Vertriebskunde_ID_UN (Vertriebskunde_ID)
</text>
<line x1="0" y1="94" x2="179" y2="94" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="101" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#92B0C5FC-140E14D85F0C" >
<text x="16" y="107" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebskunde_Vertriebsteilnehmer_FK (Vertriebsteilnehmer_Vertriebsteilnehmer_ID)
</text></a>
<polygon points="173,97 169,89 177,89" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="113" x2="179" y2="113" fill="none" stroke="rgb(0,0,255)"/>
<text x="2" y="126" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
U
</text>
<text x="16" y="126" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebskunde__IDX (Besitzer_Besitzer_ID)
</text>
<polygon points="173,97 169,89 177,89" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(153,255,0)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath22_0_)" transform="translate(1024,1199)" >
<rect x="0" y="0" width="112" height="52" />
<text id="DA001BC9-C97E68A0C482" x="20" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Ländergruppe
</text>
<line x1="0" y1="17" x2="111" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Typ
</text>
<text x="190" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Zweck
</text>
<text x="190" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="56" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Ländergruppe_ID
</text>
<text x="190" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="105,49 101,41 109,41" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="62" x2="111" y2="62" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="69" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="75" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Ländergruppe_PK (Geografische_Einheit_GEIN_ID, Ländergruppe_ID)
</text>
<polygon points="105,49 101,41 109,41" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="81" x2="111" y2="81" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="88" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#4623645A-68B64E30D79B" >
<text x="16" y="94" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Ländergruppe_Geografische_Einheit_FK (Geografische_Einheit_GEIN_ID)
</text></a>
<polygon points="105,49 101,41 109,41" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath13_0_)" transform="translate(1455,1692)" >
<rect x="0" y="0" width="110" height="27" />
<text id="96CF5C69-9CA5ECFDD8CD" x="34" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Händler
</text>
<line x1="0" y1="17" x2="109" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Handelseinheit_Handelseinheit_ID
</text>
<text x="212" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="103,24 99,16 107,16" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="36" x2="109" y2="36" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="43" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="49" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Händler_PK (Handelseinheit_Handelseinheit_ID)
</text>
<polygon points="103,24 99,16 107,16" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="55" x2="109" y2="55" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="62" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#B730B6D1-784FA44EFCEA" >
<text x="16" y="68" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Händler_Handelseinheit_FK (Handelseinheit_Handelseinheit_ID)
</text></a>
<polygon points="103,24 99,16 107,16" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(203,218,124)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath42_0_)" transform="translate(616,1720)" >
<rect x="0" y="0" width="130" height="67" />
<text id="4A2A6CE7-04C069508D0D" x="43" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Standort
</text>
<line x1="0" y1="17" x2="129" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Name
</text>
<text x="393" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Standort_ID
</text>
<text x="393" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Juristische_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID
</text>
<text x="393" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="69" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Juristische_Person_Juristische_Person_ID
</text>
<text x="393" y="69" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="123,64 119,56 127,56" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="75" x2="129" y2="75" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="82" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="88" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Standort_PK (Standort_ID)
</text>
<polygon points="123,64 119,56 127,56" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="94" x2="129" y2="94" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="101" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#3791AFE5-FA89BDDBAB70" >
<text x="16" y="107" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Standort_Juristische_Person_FK (Juristische_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID, Juristische_Person_Juristische_Person_ID)
</text></a>
<polygon points="123,64 119,56 127,56" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="113" x2="129" y2="113" fill="none" stroke="rgb(0,0,255)"/>
<text x="2" y="126" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
U
</text>
<text x="16" y="126" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Standort__IDX (Kommunikationsmittel_Kommunikationsmittel_ID)
</text>
<polygon points="123,64 119,56 127,56" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(255,255,180)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath37_0_)" transform="translate(1668,1327)" >
<rect x="0" y="0" width="169" height="109" />
<text id="79476DC0-398CC38907C8" x="54" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Relation_53
</text>
<line x1="0" y1="17" x2="168" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Geografische_Einheit_GEIN_ID
</text>
<text x="212" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Handelseinheit_Handelseinheit_ID
</text>
<text x="212" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="49" x2="168" y2="49" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="56" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="62" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_53_PK (Geografische_Einheit_GEIN_ID, Handelseinheit_Handelseinheit_ID)
</text>
<line x1="0" y1="68" x2="168" y2="68" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="75" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#4623645A-68B64E30D79B" >
<text x="16" y="81" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_53_Geografische_Einheit_FK (Geografische_Einheit_GEIN_ID)
</text></a>
<use xlink:href="#fk_sym" x="4" y="88" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#B730B6D1-784FA44EFCEA" >
<text x="16" y="94" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_53_Handelseinheit_FK (Handelseinheit_Handelseinheit_ID)
</text></a>
</g>
<g  fill="rgb(203,218,124)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath27_0_)" transform="translate(1379,1152)" >
<rect x="0" y="0" width="128" height="78" />
<text id="4E447132-09B3FE5665A4" x="46" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
person
</text>
<line x1="0" y1="17" x2="127" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vorname
</text>
<text x="300" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
date_of_birth
</text>
<text x="300" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Geschlecht
</text>
<text x="300" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="69" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="69" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
natürliche_Person_ID
</text>
<text x="300" y="69" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="82" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="82" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="82" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID
</text>
<text x="300" y="82" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="121,75 117,67 125,67" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="88" x2="127" y2="88" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="95" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="101" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
natürliche_Person_PK (Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID, natürliche_Person_ID)
</text>
<polygon points="121,75 117,67 125,67" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="107" x2="127" y2="107" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="114" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#38FC9743-5D02070CB9D4" >
<text x="16" y="120" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
natürliche_Person_Geschäftsfähige_Einheit_FK (Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID)
</text></a>
<polygon points="121,75 117,67 125,67" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath8_0_)" transform="translate(2891,1191)" >
<rect x="0" y="0" width="152" height="26" />
<text id="58D043C6-B1AFF77615FF" x="20" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Finanzierungspartner
</text>
<line x1="0" y1="17" x2="151" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebsteilnehmer_Vertriebsteilnehmer_ID
</text>
<text x="262" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="145,23 141,15 149,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="36" x2="151" y2="36" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="43" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="49" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Finanzierungspartner_PK (Vertriebsteilnehmer_Vertriebsteilnehmer_ID)
</text>
<polygon points="145,23 141,15 149,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="55" x2="151" y2="55" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="62" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#92B0C5FC-140E14D85F0C" >
<text x="16" y="68" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Finanzierungspartner_Vertriebsteilnehmer_FK (Vertriebsteilnehmer_Vertriebsteilnehmer_ID)
</text></a>
<polygon points="145,23 141,15 149,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath41_0_)" transform="translate(2014,2182)" >
<rect x="0" y="0" width="110" height="29" />
<text id="2E47F8A2-D711B5826B42" x="20" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Servicepartner
</text>
<line x1="0" y1="17" x2="109" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Handelseinheit_Handelseinheit_ID
</text>
<text x="212" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
U
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Servicepartner_ID
</text>
<text x="212" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="103,26 99,18 107,18" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="49" x2="109" y2="49" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="56" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="62" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Servicepartner_PK (Handelseinheit_Handelseinheit_ID)
</text>
<polygon points="103,26 99,18 107,18" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="68" x2="109" y2="68" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="75" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#B730B6D1-784FA44EFCEA" >
<text x="16" y="81" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Servicepartner_Handelseinheit_FK (Handelseinheit_Handelseinheit_ID)
</text></a>
<polygon points="103,26 99,18 107,18" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(255,255,180)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath34_0_)" transform="translate(2672,1715)" >
<rect x="0" y="0" width="169" height="112" />
<text id="DFBE6461-8F9498119346" x="51" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Relation_111
</text>
<line x1="0" y1="17" x2="168" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Wettbewerber_Wettbewerber_ID
</text>
<text x="204" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Interessent_Interessent_ID
</text>
<text x="204" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="49" x2="168" y2="49" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="56" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="62" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_111_PK (Wettbewerber_Wettbewerber_ID, Interessent_Interessent_ID)
</text>
<line x1="0" y1="68" x2="168" y2="68" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="75" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#A23A66C0-AA46743F4C07" >
<text x="16" y="81" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_111_Wettbewerber_FK (Wettbewerber_Wettbewerber_ID)
</text></a>
<use xlink:href="#fk_sym" x="4" y="88" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#C5F5C08D-A2771073ED98" >
<text x="16" y="94" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_111_Interessent_FK (Interessent_Interessent_ID)
</text></a>
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath44_0_)" transform="translate(2494,1191)" >
<rect x="0" y="0" width="125" height="50" />
<text id="BB68FE87-4EF1D4AD7ADB" x="20" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Vertriebspartner
</text>
<line x1="0" y1="17" x2="124" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebspartner_ID
</text>
<text x="262" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebsteilnehmer_Vertriebsteilnehmer_ID
</text>
<text x="262" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="49" x2="124" y2="49" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="56" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="62" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebspartner_PK (Vertriebsteilnehmer_Vertriebsteilnehmer_ID, Vertriebspartner_ID)
</text>
<polygon points="118,47 114,39 122,39" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="68" x2="124" y2="68" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="75" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#92B0C5FC-140E14D85F0C" >
<text x="16" y="81" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebspartner_Vertriebsteilnehmer_FK (Vertriebsteilnehmer_Vertriebsteilnehmer_ID)
</text></a>
<polygon points="118,47 114,39 122,39" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(203,218,124)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath28_0_)" transform="translate(20,637)" >
<rect x="0" y="0" width="136" height="63" />
<text id="3408EC76-F74DE9AC1DD8" x="32" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Personenrolle
</text>
<line x1="0" y1="17" x2="135" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Bezeichnung
</text>
<text x="128" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Beschreibung
</text>
<text x="128" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="56" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Personenrolle_ID
</text>
<text x="128" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="62" x2="135" y2="62" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="69" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="75" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Personenrolle_PK (Personenrolle_ID)
</text>
<polygon points="129,60 125,52 133,52" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(255,255,180)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath40_0_)" transform="translate(2589,1302)" >
<rect x="0" y="0" width="169" height="109" />
<text id="EE0AE4E9-E6992ECD752D" x="54" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Relation_62
</text>
<line x1="0" y1="17" x2="168" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebspartner_Vertriebsteilnehmer_Vertriebsteilnehmer_ID
</text>
<text x="348" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebspartner_Vertriebspartner_ID
</text>
<text x="348" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="56" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID
</text>
<text x="348" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="69" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="69" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebskunde_Vertriebskunde_ID
</text>
<text x="348" y="69" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="75" x2="168" y2="75" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="82" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="88" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_62_PK (Vertriebspartner_Vertriebsteilnehmer_Vertriebsteilnehmer_ID, Vertriebspartner_Vertriebspartner_ID, Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID, Vertriebskunde_Vertriebskunde_ID)
</text>
<line x1="0" y1="94" x2="168" y2="94" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="101" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#BB68FE87-4EF1D4AD7ADB" >
<text x="16" y="107" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_62_Vertriebspartner_FK (Vertriebspartner_Vertriebsteilnehmer_Vertriebsteilnehmer_ID, Vertriebspartner_Vertriebspartner_ID)
</text></a>
<use xlink:href="#fk_sym" x="4" y="114" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#E4C6AAFE-6B5E5EF62F40" >
<text x="16" y="120" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_62_Vertriebskunde_FK (Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID, Vertriebskunde_Vertriebskunde_ID)
</text></a>
<polygon points="162,106 158,98 166,98" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(203,218,124)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath14_0_)" transform="translate(1503,1004)" >
<rect x="0" y="0" width="136" height="63" />
<text id="F8C5905E-281E392B3111" x="45" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Haushalt
</text>
<line x1="0" y1="17" x2="135" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Haushalt_ID
</text>
<text x="104" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="36" x2="135" y2="36" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="43" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="49" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Haushalt_PK (Haushalt_ID)
</text>
</g>
<g  fill="rgb(153,255,0)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath29_0_)" transform="translate(1023,752)" >
<rect x="0" y="0" width="142" height="52" />
<text id="C0B4ACF6-15D198ED9BD8" x="43" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
PLZ-Gebiet
</text>
<line x1="0" y1="17" x2="141" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Postleitzahl
</text>
<text x="227" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
PLZ-Ebene
</text>
<text x="227" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="56" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
PLZ-Gebiet_ID
</text>
<text x="227" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="135,49 131,41 139,41" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="62" x2="141" y2="62" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="69" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="75" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
PLZ-Gebiet_PK (Gebiet_Geografische_Einheit_GEIN_ID, PLZ-Gebiet_ID)
</text>
<polygon points="135,49 131,41 139,41" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="81" x2="141" y2="81" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="88" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#616FBC25-5093773E214A" >
<text x="16" y="94" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
PLZ-Gebiet_Gebiet_FK (Gebiet_Geografische_Einheit_GEIN_ID)
</text></a>
<polygon points="135,49 131,41 139,41" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(255,255,180)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath35_0_)" transform="translate(20,467)" >
<rect x="0" y="0" width="169" height="109" />
<text id="287C0437-6D84B613815E" x="54" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Relation_46
</text>
<line x1="0" y1="17" x2="168" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Ansprechpartner_Ansprechpartner_ID
</text>
<text x="228" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Personenrolle_Personenrolle_ID
</text>
<text x="228" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="49" x2="168" y2="49" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="56" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="62" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_46_PK (Ansprechpartner_Ansprechpartner_ID, Personenrolle_Personenrolle_ID)
</text>
<line x1="0" y1="68" x2="168" y2="68" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="75" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#FA90040D-641F12C234A3" >
<text x="16" y="81" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_46_Ansprechpartner_FK (Ansprechpartner_Ansprechpartner_ID)
</text></a>
<use xlink:href="#fk_sym" x="4" y="88" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#3408EC76-F74DE9AC1DD8" >
<text x="16" y="94" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_46_Personenrolle_FK (Personenrolle_Personenrolle_ID)
</text></a>
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath25_0_)" transform="translate(3124,1191)" >
<rect x="0" y="0" width="72" height="26" />
<text id="2E510FC7-A21C3CA81706" x="20" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Nutzer
</text>
<line x1="0" y1="17" x2="71" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebsteilnehmer_Vertriebsteilnehmer_ID
</text>
<text x="262" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="65,23 61,15 69,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="36" x2="71" y2="36" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="43" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="49" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Nutzer_PK (Vertriebsteilnehmer_Vertriebsteilnehmer_ID)
</text>
<polygon points="65,23 61,15 69,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="55" x2="71" y2="55" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="62" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#92B0C5FC-140E14D85F0C" >
<text x="16" y="68" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Nutzer_Vertriebsteilnehmer_FK (Vertriebsteilnehmer_Vertriebsteilnehmer_ID)
</text></a>
<polygon points="65,23 61,15 69,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath23_0_)" transform="translate(1863,1352)" >
<rect x="0" y="0" width="118" height="26" />
<text id="BA02059E-B07A74E4D45C" x="20" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Leasingnehmer
</text>
<line x1="0" y1="17" x2="117" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID
</text>
<text x="342" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="111,23 107,15 115,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="36" x2="117" y2="36" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="43" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="49" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Leasingnehmer_PK (Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID)
</text>
<polygon points="111,23 107,15 115,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="55" x2="117" y2="55" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="62" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#E4C6AAFE-6B5E5EF62F40" >
<text x="16" y="68" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Leasingnehmer_Vertriebskunde_FK (Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID)
</text></a>
<polygon points="111,23 107,15 115,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(203,218,124)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath18_0_)" transform="translate(857,1637)" >
<rect x="0" y="0" width="131" height="83" />
<text id="3791AFE5-FA89BDDBAB70" x="20" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Juristische_Person
</text>
<line x1="0" y1="17" x2="130" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Gesellschaftsform
</text>
<text x="300" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
UID_Nr
</text>
<text x="300" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="56" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Juristische_Person_ID
</text>
<text x="300" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="69" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="69" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID
</text>
<text x="300" y="69" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="75" x2="130" y2="75" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="82" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="88" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Juristische_Person_PK (Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID, Juristische_Person_ID)
</text>
<polygon points="124,80 120,72 128,72" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="94" x2="130" y2="94" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="101" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#38FC9743-5D02070CB9D4" >
<text x="16" y="107" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Juristische_Person_Geschäftsfähige_Einheit_FK (Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID)
</text></a>
<polygon points="124,80 120,72 128,72" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath6_0_)" transform="translate(2891,1278)" >
<rect x="0" y="0" width="110" height="59" />
<text id="5F5A46F2-0F0F43ECD471" x="25" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Eigentümer
</text>
<line x1="0" y1="17" x2="109" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Eigentümer_ID
</text>
<text x="380" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="2" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Finanzierungspartner_Vertriebsteilnehmer_Vertriebsteilnehmer_ID
</text>
<text x="380" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="2" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebspartner_Vertriebsteilnehmer_Vertriebsteilnehmer_ID
</text>
<text x="380" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="69" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="2" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Käufer_Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID
</text>
<text x="380" y="69" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="103,56 99,48 107,48" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="75" x2="109" y2="75" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="82" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="88" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Eigentümer_PK (Eigentümer_ID)
</text>
<polygon points="103,56 99,48 107,48" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="94" x2="109" y2="94" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="101" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#58D043C6-B1AFF77615FF" >
<text x="16" y="107" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Eigentümer_Finanzierungspartner_FK (Finanzierungspartner_Vertriebsteilnehmer_Vertriebsteilnehmer_ID)
</text></a>
<polygon points="103,56 99,48 107,48" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="113" x2="109" y2="113" fill="none" stroke="rgb(0,0,255)"/>
<text x="2" y="126" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
U
</text>
<text x="16" y="126" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Eigentümer__IDX (Finanzierungspartner_Vertriebsteilnehmer_Vertriebsteilnehmer_ID)
</text>
<polygon points="103,56 99,48 107,48" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath7_0_)" transform="translate(1264,1692)" >
<rect x="0" y="0" width="110" height="27" />
<text id="9CAA3C40-90F379DD2F0B" x="40" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Filiale
</text>
<line x1="0" y1="17" x2="109" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Handelseinheit_Handelseinheit_ID
</text>
<text x="212" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="103,24 99,16 107,16" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="36" x2="109" y2="36" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="43" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="49" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Filiale_PK (Handelseinheit_Handelseinheit_ID)
</text>
<polygon points="103,24 99,16 107,16" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="55" x2="109" y2="55" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="62" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#B730B6D1-784FA44EFCEA" >
<text x="16" y="68" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Filiale_Handelseinheit_FK (Handelseinheit_Handelseinheit_ID)
</text></a>
<polygon points="103,24 99,16 107,16" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(153,255,0)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath10_0_)" transform="translate(1333,284)" >
<rect x="0" y="0" width="357" height="370" />
<text id="4623645A-68B64E30D79B" x="124" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Geografische_Einheit
</text>
<line x1="0" y1="17" x2="356" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
GEIN_ID
</text>
<text x="122" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Name_[L]
</text>
<text x="122" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
VARCHAR2 (60)
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
GeoInformation
</text>
<text x="122" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<line x1="0" y1="62" x2="356" y2="62" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="69" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="75" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
GEIN_PK (GEIN_ID)
</text>
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath5_0_)" transform="translate(2398,1302)" >
<rect x="0" y="0" width="110" height="59" />
<text id="ED3FC77A-C8FAB0739751" x="34" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Besitzer
</text>
<line x1="0" y1="17" x2="109" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Besitzer_ID
</text>
<text x="348" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="2" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID
</text>
<text x="348" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="2" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebskunde_Vertriebskunde_ID
</text>
<text x="348" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="69" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="2" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebspartner_Vertriebsteilnehmer_Vertriebsteilnehmer_ID
</text>
<text x="348" y="69" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="103,56 99,48 107,48" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="75" x2="109" y2="75" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="82" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="88" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Besitzer_PK (Besitzer_ID)
</text>
<polygon points="103,56 99,48 107,48" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="94" x2="109" y2="94" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="101" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#E4C6AAFE-6B5E5EF62F40" >
<text x="16" y="107" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Besitzer_Vertriebskunde_FK (Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID, Vertriebskunde_Vertriebskunde_ID)
</text></a>
<polygon points="103,56 99,48 107,48" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="113" x2="109" y2="113" fill="none" stroke="rgb(0,0,255)"/>
<text x="2" y="126" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
U
</text>
<text x="16" y="126" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Besitzer__IDX (Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID, Vertriebskunde_Vertriebskunde_ID)
</text>
<polygon points="103,56 99,48 107,48" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(203,218,124)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath26_0_)" transform="translate(583,330)" >
<rect x="0" y="0" width="136" height="63" />
<text id="C0BF57A2-DC6F635193E1" x="20" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Organisationseinheit
</text>
<line x1="0" y1="17" x2="135" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Name
</text>
<text x="393" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Organisationseinheit_ID
</text>
<text x="393" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
bild1v6v1_bild1v6v1_ID
</text>
<text x="393" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="69" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Juristische_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID
</text>
<text x="393" y="69" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="129,60 125,52 133,52" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="75" x2="135" y2="75" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="82" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="88" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Organisationseinheit_PK (Organisationseinheit_ID)
</text>
<polygon points="129,60 125,52 133,52" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="94" x2="135" y2="94" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="101" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#3791AFE5-FA89BDDBAB70" >
<text x="16" y="107" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Organisationseinheit_Juristische_Person_FK (Juristische_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID, Juristische_Person_Juristische_Person_ID)
</text></a>
<polygon points="129,60 125,52 133,52" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="113" x2="135" y2="113" fill="none" stroke="rgb(0,0,255)"/>
<text x="2" y="126" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
U
</text>
<text x="16" y="126" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Organisationseinheit__IDX (bild1v6v1_bild1v6v1_ID)
</text>
<polygon points="129,60 125,52 133,52" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath24_0_)" transform="translate(2062,1352)" >
<rect x="0" y="0" width="69" height="26" />
<text id="5982D485-4B124D297779" x="20" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Mieter
</text>
<line x1="0" y1="17" x2="68" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID
</text>
<text x="342" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="62,23 58,15 66,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="36" x2="68" y2="36" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="43" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="49" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Mieter_PK (Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID)
</text>
<polygon points="62,23 58,15 66,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="55" x2="68" y2="55" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="62" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#E4C6AAFE-6B5E5EF62F40" >
<text x="16" y="68" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Mieter_Vertriebskunde_FK (Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID)
</text></a>
<polygon points="62,23 58,15 66,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath12_0_)" transform="translate(1908,1830)" >
<rect x="0" y="0" width="270" height="193" />
<text id="B730B6D1-784FA44EFCEA" x="96" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Handelseinheit
</text>
<line x1="0" y1="17" x2="269" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Handelseinheit_ID
</text>
<text x="348" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Professionalisierungsgrad
</text>
<text x="348" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="2" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebspartner_Vertriebsteilnehmer_Vertriebsteilnehmer_ID
</text>
<text x="348" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="69" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="2" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebspartner_Vertriebspartner_ID
</text>
<text x="348" y="69" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="82" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="2" y="82" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="82" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Wettbewerber_Wettbewerber_ID
</text>
<text x="348" y="82" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="88" x2="269" y2="88" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="95" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="101" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Handelseinheit_PK (Handelseinheit_ID)
</text>
<line x1="0" y1="107" x2="269" y2="107" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="114" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#BB68FE87-4EF1D4AD7ADB" >
<text x="16" y="120" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Handelseinheit_Vertriebspartner_FK (Vertriebspartner_Vertriebsteilnehmer_Vertriebsteilnehmer_ID, Vertriebspartner_Vertriebspartner_ID)
</text></a>
<use xlink:href="#fk_sym" x="4" y="127" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#A23A66C0-AA46743F4C07" >
<text x="16" y="133" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Handelseinheit_Wettbewerber_FK (Wettbewerber_Wettbewerber_ID)
</text></a>
</g>
<g  fill="rgb(255,255,180)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath36_0_)" transform="translate(2148,1191)" >
<rect x="0" y="0" width="169" height="109" />
<text id="483BA939-CB0BAFFB304C" x="54" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Relation_48
</text>
<line x1="0" y1="17" x2="168" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Handelseinheit_Handelseinheit_ID
</text>
<text x="262" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebsteilnehmer_Vertriebsteilnehmer_ID
</text>
<text x="262" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="49" x2="168" y2="49" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="56" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="62" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_48_PK (Handelseinheit_Handelseinheit_ID, Vertriebsteilnehmer_Vertriebsteilnehmer_ID)
</text>
<line x1="0" y1="68" x2="168" y2="68" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="75" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#B730B6D1-784FA44EFCEA" >
<text x="16" y="81" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_48_Handelseinheit_FK (Handelseinheit_Handelseinheit_ID)
</text></a>
<use xlink:href="#fk_sym" x="4" y="88" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#92B0C5FC-140E14D85F0C" >
<text x="16" y="94" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_48_Vertriebsteilnehmer_FK (Vertriebsteilnehmer_Vertriebsteilnehmer_ID)
</text></a>
</g>
<g  fill="rgb(153,255,0)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath9_0_)" transform="translate(1023,865)" >
<rect x="0" y="0" width="190" height="134" />
<text id="616FBC25-5093773E214A" x="79" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Gebiet
</text>
<line x1="0" y1="17" x2="189" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Geografische_Einheit_GEIN_ID
</text>
<text x="227" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
U
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Gebiet_ID
</text>
<text x="227" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Land_Geografische_Einheit_GEIN_ID
</text>
<text x="227" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="69" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Land_LAND_ID
</text>
<text x="227" y="69" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="82" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="2" y="82" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="82" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Gebiet_Geografische_Einheit_GEIN_ID
</text>
<text x="227" y="82" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="88" x2="189" y2="88" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="95" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="101" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Gebiet_PK (Geografische_Einheit_GEIN_ID)
</text>
<use xlink:href="#uk_sym" x="4" y="108" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="114" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Gebiet_Gebiet_ID_UN (Gebiet_ID)
</text>
<line x1="0" y1="120" x2="189" y2="120" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="127" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#4623645A-68B64E30D79B" >
<text x="16" y="133" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Gebiet_Geografische_Einheit_FK (Geografische_Einheit_GEIN_ID)
</text></a>
<use xlink:href="#fk_sym" x="4" y="140" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#19B5F296-1D5FC327C71A" >
<text x="16" y="146" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Gebiet_Land_FK (Land_Geografische_Einheit_GEIN_ID, Land_LAND_ID)
</text></a>
<polygon points="183,131 179,123 187,123" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath3_0_)" transform="translate(1857,1670)" >
<rect x="0" y="0" width="110" height="26" />
<text id="6FE73FE2-D227280DE9FD" x="40" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Agent
</text>
<line x1="0" y1="17" x2="109" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Handelseinheit_Handelseinheit_ID
</text>
<text x="212" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="103,23 99,15 107,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="36" x2="109" y2="36" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="43" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="49" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Agent_PK (Handelseinheit_Handelseinheit_ID)
</text>
<polygon points="103,23 99,15 107,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="55" x2="109" y2="55" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="62" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#B730B6D1-784FA44EFCEA" >
<text x="16" y="68" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Agent_Handelseinheit_FK (Handelseinheit_Handelseinheit_ID)
</text></a>
<polygon points="103,23 99,15 107,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(153,255,0)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath1_0_)" transform="translate(800,1060)" >
<rect x="0" y="0" width="142" height="52" />
<text id="A9178943-A6B967DF23BB" x="20" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Administrativgebiet
</text>
<line x1="0" y1="17" x2="141" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Gebiet_Geografische_Einheit_GEIN_ID
</text>
<text x="227" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Administrativebene
</text>
<text x="227" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="56" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
U
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Administrativgebiet_ID
</text>
<text x="227" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="135,49 131,41 139,41" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="62" x2="141" y2="62" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="69" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="75" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Administrativgebiet_PK (Gebiet_Geografische_Einheit_GEIN_ID)
</text>
<polygon points="135,49 131,41 139,41" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="81" x2="141" y2="81" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="88" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#616FBC25-5093773E214A" >
<text x="16" y="94" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Administrativgebiet_Gebiet_FK (Gebiet_Geografische_Einheit_GEIN_ID)
</text></a>
<polygon points="135,49 131,41 139,41" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(203,218,124)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath20_0_)" transform="translate(339,1985)" >
<rect x="0" y="0" width="146" height="80" />
<text id="4B8B3C74-CEEE2315D8E7" x="20" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Kommunikationsmittel
</text>
<line x1="0" y1="17" x2="145" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
eMail
</text>
<text x="300" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Fixnet_Tel_Nr
</text>
<text x="300" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Mobil_Tel_Nr
</text>
<text x="300" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="69" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Webseite
</text>
<text x="300" y="69" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="82" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="82" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="82" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Kommunikationsmittel_ID
</text>
<text x="300" y="82" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="139,77 135,69 143,69" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="88" x2="145" y2="88" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="95" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="101" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Kommunikationsmittel_PK (Kommunikationsmittel_ID)
</text>
<polygon points="139,77 135,69 143,69" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="107" x2="145" y2="107" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="114" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#38FC9743-5D02070CB9D4" >
<text x="16" y="120" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Kommunikationsmittel_Geschäftsfähige_Einheit_FK (Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID)
</text></a>
<polygon points="139,77 135,69 143,69" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="126" x2="145" y2="126" fill="none" stroke="rgb(0,0,255)"/>
<text x="2" y="139" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
U
</text>
<text x="16" y="139" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Kommunikationsmittel__IDX (Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID)
</text>
<polygon points="139,77 135,69 143,69" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(255,153,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath31_0_)" transform="translate(2700,1398)" >
<rect x="0" y="0" width="110" height="59" />
<text id="034D5BEE-DE0D3271FD40" x="20" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Produktinstanz
</text>
<line x1="0" y1="17" x2="109" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Serie-Nr
</text>
<text x="176" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Produktinstanz_ID
</text>
<text x="176" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="2" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Besitzer_Besitzer_ID
</text>
<text x="176" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="69" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="2" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Eigentümer_Eigentümer_ID
</text>
<text x="176" y="69" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="103,56 99,48 107,48" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="75" x2="109" y2="75" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="82" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="88" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Produktinstanz_PK (Produktinstanz_ID)
</text>
<polygon points="103,56 99,48 107,48" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="94" x2="109" y2="94" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="101" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#ED3FC77A-C8FAB0739751" >
<text x="16" y="107" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Produktinstanz_Besitzer_FK (Besitzer_Besitzer_ID)
</text></a>
<polygon points="103,56 99,48 107,48" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath30_0_)" transform="translate(3070,1021)" >
<rect x="0" y="0" width="160" height="26" />
<text id="9D6529BD-EBCDFDECA13C" x="20" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Potenzieller_Interessent
</text>
<line x1="0" y1="17" x2="159" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Interessent_Interessent_ID
</text>
<text x="180" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="153,23 149,15 157,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="36" x2="159" y2="36" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="43" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="49" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Potenzieller_Interessent_PK (Interessent_Interessent_ID)
</text>
<polygon points="153,23 149,15 157,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="55" x2="159" y2="55" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="62" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#C5F5C08D-A2771073ED98" >
<text x="16" y="68" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Potenzieller_Interessent_Interessent_FK (Interessent_Interessent_ID)
</text></a>
<polygon points="153,23 149,15 157,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath15_0_)" transform="translate(1646,1692)" >
<rect x="0" y="0" width="110" height="27" />
<text id="34FFB858-9CFAD1016B23" x="29" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Importeur
</text>
<line x1="0" y1="17" x2="109" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Handelseinheit_Handelseinheit_ID
</text>
<text x="212" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="103,24 99,16 107,16" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="36" x2="109" y2="36" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="43" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="49" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Importeur_PK (Handelseinheit_Handelseinheit_ID)
</text>
<polygon points="103,24 99,16 107,16" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="55" x2="109" y2="55" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="62" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#B730B6D1-784FA44EFCEA" >
<text x="16" y="68" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Importeur_Handelseinheit_FK (Handelseinheit_Handelseinheit_ID)
</text></a>
<polygon points="103,24 99,16 107,16" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath16_0_)" transform="translate(1823,2182)" >
<rect x="0" y="0" width="110" height="29" />
<text id="F34E49B6-8FFE27D65CDE" x="25" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Installateur
</text>
<line x1="0" y1="17" x2="109" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Handelseinheit_Handelseinheit_ID
</text>
<text x="212" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
U
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Installateur_ID
</text>
<text x="212" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="103,26 99,18 107,18" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="49" x2="109" y2="49" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="56" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="62" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Installateur_PK (Handelseinheit_Handelseinheit_ID)
</text>
<polygon points="103,26 99,18 107,18" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="68" x2="109" y2="68" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="75" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#B730B6D1-784FA44EFCEA" >
<text x="16" y="81" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Installateur_Handelseinheit_FK (Handelseinheit_Handelseinheit_ID)
</text></a>
<polygon points="103,26 99,18 107,18" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath19_0_)" transform="translate(2235,985)" >
<rect x="0" y="0" width="71" height="26" />
<text id="C297FED9-D4C3114CB153" x="20" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Käufer
</text>
<line x1="0" y1="17" x2="70" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID
</text>
<text x="342" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="64,23 60,15 68,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="36" x2="70" y2="36" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="43" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="49" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Käufer_PK (Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID)
</text>
<polygon points="64,23 60,15 68,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="55" x2="70" y2="55" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="62" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#E4C6AAFE-6B5E5EF62F40" >
<text x="16" y="68" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Käufer_Vertriebskunde_FK (Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID)
</text></a>
<polygon points="64,23 60,15 68,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="74" x2="70" y2="74" fill="none" stroke="rgb(0,0,255)"/>
<text x="2" y="87" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
U
</text>
<text x="16" y="87" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Käufer__IDX (Eigentümer_Eigentümer_ID)
</text>
<polygon points="64,23 60,15 68,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath46_0_)" transform="translate(2497,1584)" >
<rect x="0" y="0" width="110" height="73" />
<text id="A23A66C0-AA46743F4C07" x="20" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Wettbewerber
</text>
<line x1="0" y1="17" x2="109" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Wettbewerber_ID
</text>
<text x="300" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID
</text>
<text x="300" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="49" x2="109" y2="49" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="56" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="62" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Wettbewerber_PK (Wettbewerber_ID)
</text>
<line x1="0" y1="68" x2="109" y2="68" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="75" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#38FC9743-5D02070CB9D4" >
<text x="16" y="81" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Wettbewerber_Geschäftsfähige_Einheit_FK (Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID)
</text></a>
<polygon points="103,70 99,62 107,62" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath17_0_)" transform="translate(3191,865)" >
<rect x="0" y="0" width="191" height="95" />
<text id="C5F5C08D-A2771073ED98" x="66" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Interessent
</text>
<line x1="0" y1="17" x2="190" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Interessent_ID
</text>
<text x="300" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID
</text>
<text x="300" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="49" x2="190" y2="49" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="56" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="62" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Interessent_PK (Interessent_ID)
</text>
<line x1="0" y1="68" x2="190" y2="68" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="75" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#38FC9743-5D02070CB9D4" >
<text x="16" y="81" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Interessent_Geschäftsfähige_Einheit_FK (Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID)
</text></a>
</g>
<g  fill="rgb(255,255,180)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath33_0_)" transform="translate(1078,1566)" >
<rect x="0" y="0" width="169" height="113" />
<text id="4F452D3C-CF2EAD28C059" x="58" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Relation_1
</text>
<line x1="0" y1="17" x2="168" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Juristische_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID
</text>
<text x="399" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Juristische_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID1
</text>
<text x="399" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="49" x2="168" y2="49" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="56" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="62" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_1_PK (Juristische_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID, Juristische_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID1)
</text>
<line x1="0" y1="68" x2="168" y2="68" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="75" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#3791AFE5-FA89BDDBAB70" >
<text x="16" y="81" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_1_Juristische_Person_FK (Juristische_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID)
</text></a>
<use xlink:href="#fk_sym" x="4" y="88" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#3791AFE5-FA89BDDBAB70" >
<text x="16" y="94" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_1_Juristische_Person_FKv1 (Juristische_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID1)
</text></a>
</g>
<g fill="none" stroke="rgb(0,0,0)" transform="translate(1003.0,845.0)" >
<circle stroke-dasharray="none" cx="90.0" cy="2.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="2.0" cy="156.60550458715602" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<path d=" M13.0 177.60553 C 13.0 177.60553 3.0 177.60553 3.0 167.60553 L3.0 14.0 C 3.0 14.0 3.0 3.0 17.0 3.0 L101.0 3.0 C 101.0 3.0 111.0 3.0 111.0 13.0"/>
</g>
<g fill="none" stroke="rgb(0,0,0)" transform="translate(1888.0,1810.0)" >
<circle stroke-dasharray="none" cx="236.2874149659865" cy="2.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="306.0" cy="24.389937106918296" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<path d=" M217.28735 13.0 C 217.28735 13.0 217.28735 3.0 227.28735 3.0 L293.0 3.0 C 293.0 3.0 307.0 3.0 307.0 17.0 L307.0 35.389893 C 307.0 35.389893 307.0 45.389893 297.0 45.389893"/>
</g>
<g fill="none" stroke="rgb(0,0,0)" transform="translate(2378.0,1282.0)" >
<circle stroke-dasharray="none" cx="36.56417910447772" cy="2.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="122.0" cy="2.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<path d=" M17.564209 13.0 C 17.564209 13.0 17.564209 3.0 27.564209 3.0 L133.0 3.0 C 133.0 3.0 143.0 3.0 143.0 13.0"/>
</g>
<g fill="none" stroke="rgb(0,0,0)" transform="translate(3171.0,845.0)" >
<circle stroke-dasharray="none" cx="39.0" cy="131.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="175.0" cy="131.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<path d=" M196.0 122.0 C 196.0 122.0 196.0 132.0 186.0 132.0 L30.0 132.0 C 30.0 132.0 20.0 132.0 20.0 122.0"/>
</g>
<g fill="none" stroke="rgb(0,0,0)" transform="translate(1886.0,846.0)" >
<circle stroke-dasharray="none" cx="187.0" cy="136.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="216.0" cy="100.75675675675677" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="57.0" cy="136.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<path d=" M207.0 81.756775 C 207.0 81.756775 217.0 81.756775 217.0 91.756775 L217.0 123.0 C 217.0 123.0 217.0 137.0 203.0 137.0 L48.0 137.0 C 48.0 137.0 38.0 137.0 38.0 127.0"/>
</g>
<g fill="none" stroke="rgb(0,0,0)" transform="translate(2871.0,1258.0)" >
<circle stroke-dasharray="none" cx="2.0" cy="31.047970479704873" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="2.0" cy="4.953795379537951" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="74.0" cy="2.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<path d=" M13.0 52.047974 C 13.0 52.047974 3.0 52.047974 3.0 42.047974 L3.0 14.0 C 3.0 14.0 3.0 3.0 17.0 3.0 L85.0 3.0 C 85.0 3.0 95.0 3.0 95.0 13.0"/>
</g>
<g fill="none" stroke="rgb(0,0,0)" transform="translate(1313.0,264.0)" >
<circle stroke-dasharray="none" cx="26.361904761904725" cy="406.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="82.8529411764705" cy="406.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="66.64938271604933" cy="406.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<path d=" M103.852905 397.0 C 103.852905 397.0 103.852905 407.0 93.852905 407.0 L17.361938 407.0 C 17.361938 407.0 7.3619385 407.0 7.3619385 397.0"/>
</g>
<g fill="none" stroke="rgb(0,0,0)" transform="translate(2629.0,845.0)" >
<circle stroke-dasharray="none" cx="310.0" cy="301.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="2.0" cy="70.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="9.800000000000182" cy="301.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="376.0" cy="264.7297297297298" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<path d=" M367.0 245.72974 C 367.0 245.72974 377.0 245.72974 377.0 255.72974 L377.0 288.0 C 377.0 288.0 377.0 302.0 363.0 302.0 L17.0 302.0 C 14.0 302.0 3.0 302.0 3.0 288.0 L3.0 61.0 C 3.0 61.0 3.0 51.0 13.0 51.0"/>
</g>
<g fill="none" stroke="rgb(0,0,0)" transform="translate(436.0,1373.0)" >
<circle stroke-dasharray="none" cx="314.56097560975604" cy="197.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="318.0" cy="46.674999999999955" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<path d=" M309.0 27.675049 C 309.0 27.675049 319.0 27.675049 319.0 37.67505 L319.0 184.0 C 319.0 184.0 319.0 198.0 305.0 198.0 L305.56097 198.0 C 305.56097 198.0 295.56097 198.0 295.56097 188.0"/>
</g>
<g fill="none" stroke="rgb(0,0,0)" transform="translate(1868.0,1790.0)" >
<circle stroke-dasharray="none" cx="52.0" cy="269.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="2.0" cy="63.75274725274721" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="200.0" cy="269.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="69.0" cy="2.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="2.0" cy="24.200000000000045" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="2.0" cy="82.75690607734805" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<path d=" M221.0 260.0 C 221.0 260.0 221.0 270.0 211.0 270.0 L17.0 270.0 C 17.0 270.0 3.0 270.0 3.0 256.0 L3.0 17.0 C 3.0 17.0 3.0 3.0 17.0 3.0 L80.0 3.0 C 80.0 3.0 90.0 3.0 90.0 13.0"/>
</g>

</svg>""")
m = re.search(r'<g.*"translate\((\d+),(\d+)\)".*\n<rect.*width="(\d+)".*rx="(\d+)".*\n.*<text id="{}-{}"[\d\D]*?</g>'
                            .format(re.escape("A9178943"),re.escape("A6B967DF23BB"))
              , """
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1"  width="3472" height="2212">
<defs id="dmw_defs" >
<svg id="fk_sym" viewBox="0 0 48.665 48.665" style="enable-background:new 0 0 48.665 48.665;" >
<g>
<path d="M40.332,31.592c-2.377,0-4.515,1-6.033,2.598l-17.737-8.686c0.061-0.406,0.103-0.82,0.103-1.246    c0-0.414-0.04-0.818-0.098-1.215l17.711-8.589c1.519,1.609,3.666,2.619,6.054,2.619c4.603,0,8.333-3.731,8.333-8.333    c0-4.603-3.73-8.333-8.333-8.333s-8.333,3.73-8.333,8.333c0,0.414,0.04,0.817,0.098,1.215l-17.709,8.589    c-1.519-1.609-3.666-2.619-6.054-2.619C3.73,15.925,0,19.656,0,24.258c0,4.603,3.73,8.333,8.333,8.333    c2.377,0,4.515-1,6.033-2.596l17.736,8.685c-0.062,0.406-0.104,0.82-0.104,1.245c0,4.604,3.73,8.333,8.333,8.333    s8.333-3.729,8.333-8.333C48.665,35.322,44.935,31.592,40.332,31.592z" fill="#13bf3b"/>
</g>
</svg>
<svg id="pk_sym" viewBox="0 0 480.509 480.509" style="enable-background:new 0 0 480.509 480.509;" >
<g>
<path d="M418.119,331.046c4.094,4.374,7.766,8.186,10.996,11.416c3.237,3.238,6.714,6.376,10.427,9.422   c3.71,3.042,6.427,4.568,8.135,4.568c3.241,0,9.517-4.661,18.843-13.99c9.328-9.321,13.989-15.604,13.989-18.842   c0-1.523-2.714-5.421-8.138-11.704c-5.421-6.276-12.364-13.702-20.838-22.271c-8.473-8.565-16.703-16.744-24.694-24.55   c-8.001-7.81-15.8-15.373-23.417-22.703c-7.611-7.327-11.992-11.56-13.135-12.703c-1.902-1.902-4.093-2.853-6.563-2.853   c-3.237,0-9.521,4.661-18.843,13.988c-9.328,9.322-13.989,15.605-13.989,18.843c0,1.711,1.522,4.421,4.568,8.138   c3.046,3.71,6.188,7.187,9.421,10.424c3.23,3.23,7.047,6.899,11.42,10.992c4.377,4.093,6.848,6.423,7.423,6.995l-27.408,27.404   L254.954,222.268c24.94-33.498,37.408-68.236,37.408-104.211c0-31.024-9.761-56.293-29.263-75.801   c-19.512-19.511-44.778-29.265-75.805-29.265c-30.454,0-60.244,9.042-89.363,27.119c-29.121,18.083-52.727,41.686-70.808,70.808   C9.042,140.038,0,169.828,0,200.28c0,31.029,9.753,56.286,29.265,75.803c19.511,19.517,44.777,29.27,75.801,29.27   c35.976,0,70.71-12.467,104.212-37.407l191.574,191.579c5.332,5.328,11.796,7.994,19.417,7.994c7.991,0,15.704-3.72,23.12-11.14   c7.426-7.426,11.143-15.129,11.143-23.127c0-7.617-2.666-14.092-7.994-19.417l-62.811-62.811l27.405-27.404   C411.699,324.195,414.033,326.666,418.119,331.046z M221.556,161.458c-10.656,10.657-23.601,15.987-38.828,15.987   c-7.996,0-15.896-1.812-23.7-5.43c3.617,7.808,5.426,15.706,5.426,23.7c0,15.229-5.327,28.171-15.987,38.828   c-10.66,10.655-23.606,15.986-38.831,15.986c-15.227,0-28.168-5.325-38.828-15.986c-10.657-10.657-15.987-23.599-15.987-38.828   c0-15.227,5.327-28.171,15.987-38.828C81.464,146.23,94.409,140.9,109.636,140.9c7.992,0,15.893,1.809,23.695,5.424   c-3.616-7.804-5.424-15.706-5.424-23.699c0-15.227,5.327-28.171,15.987-38.828c10.66-10.657,23.604-15.987,38.831-15.987   c15.227,0,28.171,5.327,38.828,15.987c10.657,10.66,15.987,23.601,15.987,38.828C237.539,137.852,232.209,150.797,221.556,161.458z   " fill="#ff8345"/>
</g>
</svg>
<svg id="uk_sym" viewBox="0 0 490 490" style="enable-background:new 0 0 490 490;" >
<g>
	<polygon points="236.99,11.41 0,246.348 236.99,478.678 236.99,350.609 129.864,245 236.99,139.391  " fill="#0064fb"/>
<polygon points="253.01,478.59 490,243.651 253.01,11.322 253.01,139.391 360.136,245 253.01,350.609  " fill="#0064fb"/>
</g>
</svg>
<svg id="link_sym" viewBox="0 0 1000 900" style="enable-background:new 0 0 1000 900;" >
<g>
<path fill="black" d="M660.224 422.656c6.976 16.192-0.512 35.008-16.768 42.048-16.128 6.976-34.944-0.448-41.984-16.768-8.448-19.776-20.736-37.696-36.224-53.248-64.64-64.64-177.344-64.64-241.92 0l-145.216 145.28c-66.688 66.688-66.688 175.232 0 241.984 66.688 66.688 175.104 66.752 241.92 0l92.8-92.864c12.48-12.48 32.768-12.48 45.248 0s12.48 32.768 0 45.248l-92.8 92.864c-91.648 91.648-240.832 91.52-332.416 0-91.712-91.648-91.712-240.832 0-332.48l145.216-145.28c44.352-44.416 103.424-68.864 166.272-68.864s121.792 24.448 166.208 68.864c21.248 21.312 38.016 45.952 49.664 73.216zM891.136 401.344l-145.216 145.216c-88.768 88.832-243.712 88.832-332.416 0-21.312-21.312-38.080-45.952-49.728-73.216-7.040-16.256 0.448-35.072 16.704-42.048 16.064-6.784 35.008 0.512 41.984 16.768 8.512 19.776 20.8 37.696 36.288 53.248 64.64 64.64 177.344 64.64 241.92 0l145.216-145.216c66.688-66.688 66.688-175.232 0-241.984-66.752-66.624-175.168-66.688-241.92 0l-92.8 92.864c-12.48 12.48-32.768 12.48-45.248 0s-12.48-32.768 0-45.248l92.8-92.864c45.824-45.824 105.984-68.736 166.208-68.736s120.448 22.912 166.272 68.736c91.584 91.648 91.584 240.768-0.064 332.48z" />
</g>
</svg>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath31_0_">
<rect x="0" y="0" width="111" height="60" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath38_0_">
<rect x="0" y="0" width="170" height="110" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath39_0_">
<rect x="0" y="0" width="170" height="110" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath21_0_">
<rect x="0" y="0" width="160" height="79" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath35_0_">
<rect x="0" y="0" width="170" height="110" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath41_0_">
<rect x="0" y="0" width="111" height="30" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath25_0_">
<rect x="0" y="0" width="73" height="27" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath28_0_">
<rect x="0" y="0" width="137" height="64" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath15_0_">
<rect x="0" y="0" width="111" height="28" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath18_0_">
<rect x="0" y="0" width="132" height="84" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath11_0_">
<rect x="0" y="0" width="283" height="162" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath10_0_">
<rect x="0" y="0" width="358" height="371" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath36_0_">
<rect x="0" y="0" width="170" height="110" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath42_0_">
<rect x="0" y="0" width="131" height="68" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath20_0_">
<rect x="0" y="0" width="147" height="81" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath27_0_">
<rect x="0" y="0" width="129" height="79" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath33_0_">
<rect x="0" y="0" width="170" height="114" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath8_0_">
<rect x="0" y="0" width="153" height="27" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath24_0_">
<rect x="0" y="0" width="70" height="27" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath6_0_">
<rect x="0" y="0" width="111" height="60" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath9_0_">
<rect x="0" y="0" width="191" height="135" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath3_0_">
<rect x="0" y="0" width="111" height="27" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath37_0_">
<rect x="0" y="0" width="170" height="110" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath32_0_">
<rect x="0" y="0" width="161" height="27" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath45_0_">
<rect x="0" y="0" width="341" height="266" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath13_0_">
<rect x="0" y="0" width="111" height="28" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath7_0_">
<rect x="0" y="0" width="111" height="28" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath30_0_">
<rect x="0" y="0" width="161" height="27" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath46_0_">
<rect x="0" y="0" width="111" height="74" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath1_0_">
<rect x="0" y="0" width="143" height="53" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath12_0_">
<rect x="0" y="0" width="271" height="194" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath23_0_">
<rect x="0" y="0" width="119" height="27" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath44_0_">
<rect x="0" y="0" width="126" height="51" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath29_0_">
<rect x="0" y="0" width="143" height="53" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath26_0_">
<rect x="0" y="0" width="137" height="64" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath19_0_">
<rect x="0" y="0" width="72" height="27" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath17_0_">
<rect x="0" y="0" width="192" height="96" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath2_0_">
<rect x="0" y="0" width="150" height="101" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath22_0_">
<rect x="0" y="0" width="113" height="53" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath34_0_">
<rect x="0" y="0" width="170" height="113" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath43_0_">
<rect x="0" y="0" width="181" height="101" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath5_0_">
<rect x="0" y="0" width="111" height="60" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath40_0_">
<rect x="0" y="0" width="170" height="110" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath16_0_">
<rect x="0" y="0" width="111" height="30" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath14_0_">
<rect x="0" y="0" width="137" height="64" />
</clipPath>
<clipPath clipPathUnits="userSpaceOnUse" id="clipPath4_0_">
<rect x="0" y="0" width="147" height="77" />
</clipPath>
</defs>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-dasharray="8,8" stroke-width="1" d="M2946 1218 L2946 1278" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2946 1218 2949 1224 2943 1224" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2940.0 1272.0 L2952.0 1272.0 M2940.0 1266.6000003814697 L2952.0 1266.6000003814697" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-dasharray="8,8" stroke-width="1" d="M1214 944 L1264 944 L1264 1050 L1135 1050 L1135 1000" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1214 944 1220 941 1220 947" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1141.0 1000.0 L1135.0 1012.0 L1129.0 1000.0 M1141.0 1012.5999994277954 L1129.0 1012.5999994277954" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M402 1985 L143 985" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="402 1985 399 1980 403 1980" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M149.0 989.0 L139.0 991.0 M149.89999997615814 993.5 L139.89999997615814 995.5" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M739 1444 L3191 933" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="739 1444 744 1441 744 1445" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M3192.0 938.0 L3181.0 935.0 L3190.0 928.0 M3181.5 940.0999999046326 L3179.5 930.0999999046326" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M3257 961 L2791 1715" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="3257 961 3256 967 3252 965" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2786.0 1712.0 L2797.0 1705.0 L2796.0 1718.0 M2792.2999997138977 1701.5 L2802.2999997138977 1707.5" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M2891 1282 L2285 1012" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2891 1282 2885 1282 2887 1278" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2292.0 1009.0 L2288.0 1019.0 M2296.5 1010.7999999523163 L2292.5 1020.7999999523163" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-dasharray="8,8" stroke-width="1" d="M2052 967 L2435 1302" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2052 967 2057 968 2055 972" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2428.0 1303.0 L2434.0 1295.0 M2424.4000000953674 1300.3000001907349 L2430.4000000953674 1292.3000001907349" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1400 1152 L1400 1114" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1400 1152 1397 1146 1403 1146" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1406.0 1114.0 L1400.0 1126.0 L1394.0 1114.0 M1406.0 1126.5999994277954 L1394.0 1126.5999994277954" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1391 655 L1129 1060" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1391 655 1390 661 1386 659" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1124.0 1057.0 L1135.0 1050.0 L1134.0 1063.0 M1130.2999997138977 1046.5 L1140.2999997138977 1052.5" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M2163 1830 L2163 1301" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2163 1830 2160 1824 2166 1824" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2169.0 1301.0 L2163.0 1313.0 L2157.0 1301.0 M2169.0 1313.5999994277954 L2157.0 1313.5999994277954" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M3347 961 L3347 1021" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="3347 961 3350 967 3344 967" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M3341.0 1015.0 L3353.0 1015.0 M3341.0 1009.6000003814697 L3353.0 1009.6000003814697" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M2940 1131 L2940 1191" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2940 1131 2943 1137 2937 1137" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2934.0 1185.0 L2946.0 1185.0 M2934.0 1179.6000003814697 L2946.0 1179.6000003814697" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M989 1658 L1078 1658" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="989 1658 995 1655 995 1661" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1078.0 1664.0 L1066.0 1658.0 L1078.0 1652.0 M1065.4000005722046 1664.0 L1065.4000005722046 1652.0" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M2649 916 L2087 916" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2649 916 2643 919 2643 913" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2087.0 910.0 L2099.0 916.0 L2087.0 922.0 M2099.5999994277954 910.0 L2099.5999994277954 922.0" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M739 1426 L1379 1213" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="739 1426 744 1423 744 1427" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1380.0 1218.0 L1369.0 1215.0 L1378.0 1208.0 M1369.5 1220.0999999046326 L1367.5 1210.0999999046326" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M2604 1242 L2604 1302" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2604 1242 2607 1248 2601 1248" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2598.0 1302.0 L2604.0 1290.0 L2610.0 1302.0 M2598.0 1289.4000005722046 L2610.0 1289.4000005722046" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-dasharray="8,8" stroke-width="1" d="M2509 1349 L2700 1410" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2509 1349 2514 1348 2514 1352" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2699.0 1415.0 L2690.0 1408.0 L2701.0 1405.0 M2688.5 1412.9000000953674 L2690.5 1402.9000000953674" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M2074 967 L2074 1352" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2074 967 2077 973 2071 973" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2068.0 1346.0 L2080.0 1346.0 M2068.0 1340.6000003814697 L2080.0 1340.6000003814697" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M2087 943 L2235 987" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2087 943 2092 942 2092 946" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2229.0 991.0 L2231.0 981.0 M2224.5 990.1000000238419 L2226.5 980.1000000238419" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M878 1637 L190 985" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="878 1637 872 1635 876 1631" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M194.0 981.0 L198.0 993.0 L186.0 989.0 M202.39999961853027 989.3999996185303 L194.39999961853027 997.3999996185303" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1094 752 L1094 692" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1094 752 1091 746 1097 746" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1100.0 692.0 L1094.0 704.0 L1088.0 692.0 M1100.0 704.5999994277954 L1088.0 704.5999994277954" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-dasharray="8,8" stroke-width="1" d="M720 367 L770 367 L770 444 L663 444 L663 394" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="720 367 726 364 726 370" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M669.0 394.0 L663.0 406.0 L657.0 394.0 M669.0 406.5999994277954 L657.0 406.5999994277954" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M726 1555 L857 1637" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="726 1555 732 1556 730 1560" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M854.0 1642.0 L847.0 1631.0 L860.0 1632.0 M843.5 1635.7000002861023 L849.5 1625.7000002861023" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1354 655 L1175 865" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1354 655 1353 660 1349 658" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1174.0 858.0 L1182.0 864.0 M1176.6999998092651 854.4000000953674 L1184.6999998092651 860.4000000953674" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1104 1060 L1104 1000" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1104 1060 1101 1054 1107 1054" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1110.0 1000.0 L1104.0 1012.0 L1098.0 1000.0 M1110.0 1012.5999994277954 L1098.0 1012.5999994277954" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-dasharray="8,8" stroke-width="1" d="M2497 1654 L2179 1845" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2497 1654 2493 1659 2491 1655" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2176.0 1840.0 L2189.0 1839.0 L2182.0 1850.0 M2186.5 1833.7000002861023 L2192.5 1843.7000002861023" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1406 655 L1095 1199" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1406 655 1406 661 1402 659" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1090.0 1197.0 L1099.0 1189.0 L1100.0 1201.0 M1094.1999998092651 1186.5 L1104.1999998092651 1190.5" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M452 1985 L662 1788" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="452 1985 454 1979 458 1983" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M662.0 1796.0 L654.0 1788.0 M658.4000000953674 1799.5999999046326 L650.4000000953674 1791.5999999046326" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M989 1673 L1078 1673" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="989 1673 995 1670 995 1676" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1078.0 1679.0 L1066.0 1673.0 L1078.0 1667.0 M1065.4000005722046 1679.0 L1065.4000005722046 1667.0" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1379 1179 L223 960" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1379 1179 1374 1180 1374 1176" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M224.0 955.0 L233.0 962.0 L222.0 965.0 M234.5 957.0999999046326 L232.5 967.0999999046326" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M88 637 L88 577" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="88 637 85 631 91 631" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M94.0 577.0 L88.0 589.0 L82.0 577.0 M94.0 589.5999994277954 L82.0 589.5999994277954" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M739 1443 L2649 1034" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="739 1443 744 1440 744 1444" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2650.0 1039.0 L2639.0 1036.0 L2648.0 1029.0 M2639.5 1041.0999999046326 L2637.5 1031.0999999046326" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M2649 1070 L2318 1210" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2649 1070 2645 1074 2643 1070" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2316.0 1205.0 L2328.0 1206.0 L2320.0 1215.0 M2326.5 1200.8000001907349 L2330.5 1210.8000001907349" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M471 1555 L471 1985" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="471 1555 474 1561 468 1561" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M465.0 1979.0 L477.0 1979.0 M465.0 1973.6000003814697 L477.0 1973.6000003814697" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-dasharray="8,8" stroke-width="1" d="M2300 1012 L2906 1278" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2300 1012 2306 1012 2304 1016" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2899.0 1281.0 L2903.0 1271.0 M2894.5 1279.2000000476837 L2898.5 1269.2000000476837" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-dasharray="8,8" stroke-width="1" d="M2538 1242 L2113 1830" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2538 1242 2537 1247 2533 1245" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2109.0 1827.0 L2119.0 1822.0 L2117.0 1833.0 M2115.2999997138977 1818.6000003814697 L2123.2999997138977 1824.6000003814697" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1906 898 L635 645" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1906 898 1901 899 1901 895" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M636.0 640.0 L645.0 647.0 L634.0 650.0 M646.5 642.0999999046326 L644.5 652.0999999046326" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M198 908 L480 684" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="198 908 201 903 203 907" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M483.0 688.0 L472.0 690.0 L477.0 680.0 M474.6000003814697 694.2999997138977 L468.6000003814697 686.2999997138977" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1080 1199 L1080 1139" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1080 1199 1077 1193 1083 1193" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1086.0 1139.0 L1080.0 1151.0 L1074.0 1139.0 M1086.0 1151.5999994277954 L1074.0 1151.5999994277954" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M857 1720 L747 1720" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="857 1720 851 1723 851 1717" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M747.0 1714.0 L759.0 1720.0 L747.0 1726.0 M759.5999994277954 1714.0 L759.5999994277954 1726.0" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M647 1788 L392 1985" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="647 1788 644 1793 642 1789" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M393.0 1978.0 L399.0 1986.0 M396.59999990463257 1975.3000001907349 L402.59999990463257 1983.3000001907349" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M432 1985 L1072 692" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="432 1985 432 1979 436 1981" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1077.0 694.0 L1068.0 702.0 L1067.0 690.0 M1072.8000001907349 704.5 L1062.8000001907349 700.5" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1908 1839 L1723 1720" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1908 1839 1902 1838 1904 1834" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1731.0 1718.0 L1725.0 1728.0 M1735.5 1720.6999998092651 L1729.5 1730.6999998092651" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1023 992 L914 1060" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1023 992 1019 997 1017 993" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M916.0 1052.0 L922.0 1062.0 M920.5 1049.3000001907349 L926.5 1059.3000001907349" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M2602 1658 L2680 1715" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2602 1658 2607 1659 2605 1663" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2677.0 1719.0 L2672.0 1709.0 L2683.0 1711.0 M2668.6000003814697 1712.7000002861023 L2674.6000003814697 1704.7000002861023" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1908 1870 L1544 1720" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1908 1870 1902 1870 1904 1866" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1551.0 1717.0 L1547.0 1727.0 M1555.5 1718.7999999523163 L1551.5 1728.7999999523163" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1679 655 L1679 1327" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1679 655 1682 661 1676 661" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1673.0 1327.0 L1679.0 1315.0 L1685.0 1327.0 M1673.0 1314.4000005722046 L1685.0 1314.4000005722046" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M133 908 L133 577" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="133 908 130 902 136 902" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M139.0 577.0 L133.0 589.0 L127.0 577.0 M139.0 589.5999994277954 L127.0 589.5999994277954" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M158 985 L447 1985" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="158 985 161 990 157 990" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M441.0 1981.0 L451.0 1979.0 M440.10000002384186 1976.5 L450.10000002384186 1974.5" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M2074 967 L2589 1302" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2074 967 2080 968 2078 972" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2586.0 1307.0 L2579.0 1296.0 L2592.0 1297.0 M2575.5 1300.7000002861023 L2581.5 1290.7000002861023" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1944 967 L1944 1352" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1944 967 1947 973 1941 973" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1938.0 1346.0 L1950.0 1346.0 M1938.0 1340.6000003814697 L1950.0 1340.6000003814697" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M3211 961 L3211 1021" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="3211 961 3214 967 3208 967" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M3205.0 1015.0 L3217.0 1015.0 M3205.0 1009.6000003814697 L3217.0 1009.6000003814697" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-dasharray="8,8" stroke-width="1" d="M1505 1068 L1505 1152" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1505 1068 1508 1074 1502 1074" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1499.0 1152.0 L1505.0 1140.0 L1511.0 1152.0 M1499.0 1139.4000005722046 L1511.0 1139.4000005722046" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1938 1830 L1938 1697" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1938 1830 1935 1824 1941 1824" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1944.0 1703.0 L1932.0 1703.0 M1944.0 1708.3999996185303 L1932.0 1708.3999996185303" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-dasharray="8,8" stroke-width="1" d="M2501 1242 L2501 1302" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2501 1242 2504 1248 2498 1248" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2495.0 1296.0 L2507.0 1296.0 M2495.0 1290.6000003814697 L2507.0 1290.6000003814697" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1991 1830 L1782 1437" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1991 1830 1987 1826 1991 1824" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1787.0 1435.0 L1786.0 1447.0 L1777.0 1439.0 M1791.1999998092651 1445.5 L1781.1999998092651 1449.5" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M456 1985 L456 1555" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="456 1985 453 1979 459 1979" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M462.0 1561.0 L450.0 1561.0 M462.0 1566.3999996185303 L450.0 1566.3999996185303" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M2420 1302 L2037 967" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2420 1302 2415 1301 2417 1297" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2044.0 966.0 L2038.0 974.0 M2047.5999999046326 968.6999998092651 L2041.5999999046326 976.6999998092651" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M914 1637 L658 394" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="914 1637 911 1632 915 1632" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M663.0 393.0 L660.0 404.0 L653.0 395.0 M665.0999999046326 403.5 L655.0999999046326 405.5" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M2659 1131 L2587 1191" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2659 1131 2656 1136 2654 1132" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2584.0 1187.0 L2595.0 1185.0 L2590.0 1195.0 M2592.3999996185303 1180.7000002861023 L2598.3999996185303 1188.7000002861023" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1094 865 L1094 805" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1094 865 1091 859 1097 859" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1100.0 805.0 L1094.0 817.0 L1088.0 805.0 M1100.0 817.5999994277954 L1088.0 817.5999994277954" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M2069 2024 L2069 2182" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2069 2024 2072 2030 2066 2030" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2063.0 2176.0 L2075.0 2176.0 M2063.0 2170.6000003814697 L2075.0 2170.6000003814697" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-dasharray="8,8" stroke-width="1" d="M2620 1231 L2891 1294" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2620 1231 2625 1230 2625 1234" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2885.0 1298.0 L2887.0 1288.0 M2880.5 1297.1000000238419 L2882.5 1287.1000000238419" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1921 2024 L1921 2182" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1921 2024 1924 2030 1918 2030" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1915.0 2176.0 L1927.0 2176.0 M1915.0 2170.6000003814697 L1927.0 2170.6000003814697" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1415 1152 L1415 1114" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1415 1152 1412 1146 1418 1146" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1421.0 1114.0 L1415.0 1126.0 L1409.0 1114.0 M1421.0 1126.5999994277954 L1409.0 1126.5999994277954" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M2990 1101 L3138 1191" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2990 1101 2996 1102 2994 1106" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M3130.0 1193.0 L3136.0 1183.0 M3125.5 1190.3000001907349 L3131.5 1180.3000001907349" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M739 1484 L2497 1616" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="739 1484 744 1482 744 1486" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2497.0 1621.0 L2487.0 1616.0 L2497.0 1611.0 M2486.5 1621.0 L2486.5 1611.0" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-dasharray="8,8" stroke-width="1" d="M2898 1338 L2803 1398" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="2898 1338 2894 1343 2892 1339" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M2800.0 1393.0 L2813.0 1392.0 L2806.0 1403.0 M2810.5 1386.7000002861023 L2816.5 1396.7000002861023" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g stroke-linecap="butt" >
<path stroke="rgb(0,0,0)" fill="none" stroke-opacity="1.0"  stroke-width="1" d="M1908 1885 L1365 1720" />
<polygon stroke="rgb(0,0,0)" stroke-dasharray="none" points="1908 1885 1903 1886 1903 1882" fill="rgb(0,0,0)" stroke-width="1" stroke-opacity="1.0"  />
<path stroke-dasharray="none" d="M1371.0 1716.0 L1369.0 1726.0 M1375.5 1716.8999999761581 L1373.5 1726.8999999761581" fill="white" stroke-width="1" stroke-opacity="1.0" stroke="rgb(0,0,0)" />
</g>
<g  fill="rgb(255,255,180)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath39_0_)" transform="translate(465,574)" >
<rect x="0" y="0" width="169" height="109" />
<text id="0CCF19A2-A5AB6077BA49" x="54" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Relation_61
</text>
<line x1="0" y1="17" x2="168" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Ansprechpartner_Ansprechpartner_ID
</text>
<text x="342" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID
</text>
<text x="342" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="56" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebskunde_Vertriebskunde_ID
</text>
<text x="342" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="62" x2="168" y2="62" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="69" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="75" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_61_PK (Ansprechpartner_Ansprechpartner_ID, Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID, Vertriebskunde_Vertriebskunde_ID)
</text>
<line x1="0" y1="81" x2="168" y2="81" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="88" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#FA90040D-641F12C234A3" >
<text x="16" y="94" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_61_Ansprechpartner_FK (Ansprechpartner_Ansprechpartner_ID)
</text></a>
<use xlink:href="#fk_sym" x="4" y="101" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#E4C6AAFE-6B5E5EF62F40" >
<text x="16" y="107" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_61_Vertriebskunde_FK (Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID, Vertriebskunde_Vertriebskunde_ID)
</text></a>
</g>
<g  fill="rgb(255,255,180)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath38_0_)" transform="translate(1252,1004)" >
<rect x="0" y="0" width="169" height="109" />
<text id="090552D2-19B7D8DBC5E7" x="54" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Relation_57
</text>
<line x1="0" y1="17" x2="168" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
natürliche_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID
</text>
<text x="398" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
natürliche_Person_natürliche_Person_ID
</text>
<text x="398" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="56" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
natürliche_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID1
</text>
<text x="398" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="69" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="69" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
natürliche_Person_natürliche_Person_ID1
</text>
<text x="398" y="69" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="75" x2="168" y2="75" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="82" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="88" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_57_PK (natürliche_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID, natürliche_Person_natürliche_Person_ID, natürliche_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID1, natürliche_Person_natürliche_Person_ID1)
</text>
<line x1="0" y1="94" x2="168" y2="94" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="101" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#4E447132-09B3FE5665A4" >
<text x="16" y="107" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_57_natürliche_Person_FK (natürliche_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID, natürliche_Person_natürliche_Person_ID)
</text></a>
<use xlink:href="#fk_sym" x="4" y="114" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#4E447132-09B3FE5665A4" >
<text x="16" y="120" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_57_natürliche_Person_FKv1 (natürliche_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID1, natürliche_Person_natürliche_Person_ID1)
</text></a>
<polygon points="162,106 158,98 166,98" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(203,218,124)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath4_0_)" transform="translate(76,908)" >
<rect x="0" y="0" width="146" height="76" />
<text id="FA90040D-641F12C234A3" x="28" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Ansprechpartner
</text>
<line x1="0" y1="17" x2="145" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Gültigkeitsperiode
</text>
<text x="393" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Ansprechpartner_ID
</text>
<text x="393" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Juristische_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID
</text>
<text x="393" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="69" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
natürliche_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID
</text>
<text x="393" y="69" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="82" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="82" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="82" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
natürliche_Person_natürliche_Person_ID
</text>
<text x="393" y="82" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="139,73 135,65 143,65" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="88" x2="145" y2="88" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="95" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="101" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Ansprechpartner_PK (Ansprechpartner_ID)
</text>
<polygon points="139,73 135,65 143,65" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="107" x2="145" y2="107" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="114" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#3791AFE5-FA89BDDBAB70" >
<text x="16" y="120" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Ansprechpartner_Juristische_Person_FK (Juristische_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID)
</text></a>
<polygon points="139,73 135,65 143,65" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="126" x2="145" y2="126" fill="none" stroke="rgb(0,0,255)"/>
<text x="2" y="139" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
U
</text>
<text x="16" y="139" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Ansprechpartner__IDX (Kommunikationsmittel_Kommunikationsmittel_ID)
</text>
<polygon points="139,73 135,65 143,65" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(203,218,124)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath2_0_)" transform="translate(1022,591)" >
<rect x="0" y="0" width="149" height="100" />
<text id="D9B340FA-CCE6AE3FF6E1" x="53" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Adresse
</text>
<line x1="0" y1="17" x2="148" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Adresstyp
</text>
<text x="287" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Strassenname
</text>
<text x="287" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Hausnr
</text>
<text x="287" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="69" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Gebäudename
</text>
<text x="287" y="69" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="82" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="82" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Geokoordinate
</text>
<text x="287" y="82" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="95" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="95" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="95" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Adresse_ID
</text>
<text x="287" y="95" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="108" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="108" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
bild1_bild1_ID
</text>
<text x="287" y="108" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="142,97 138,89 146,89" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="114" x2="148" y2="114" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="121" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="127" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Adresse_PK (Adresse_ID)
</text>
<polygon points="142,97 138,89 146,89" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="133" x2="148" y2="133" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="140" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#C0B4ACF6-15D198ED9BD8" >
<text x="16" y="146" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Adresse_PLZ-Gebiet_FK (PLZ-Gebiet_Gebiet_Geografische_Einheit_GEIN_ID, PLZ-Gebiet_PLZ-Gebiet_ID)
</text></a>
<polygon points="142,97 138,89 146,89" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="152" x2="148" y2="152" fill="none" stroke="rgb(0,0,255)"/>
<text x="2" y="165" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
U
</text>
<text x="16" y="165" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Adresse__IDX (bild1_bild1_ID)
</text>
<polygon points="142,97 138,89 146,89" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath45_0_)" transform="translate(2649,865)" >
<rect x="0" y="0" width="340" height="265" />
<text id="92B0C5FC-140E14D85F0C" x="117" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Vertriebsteilnehmer
</text>
<line x1="0" y1="17" x2="339" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebsteilnehmer_ID
</text>
<text x="300" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID
</text>
<text x="300" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="49" x2="339" y2="49" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="56" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="62" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebsteilnehmer_PK (Vertriebsteilnehmer_ID)
</text>
<line x1="0" y1="68" x2="339" y2="68" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="75" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#38FC9743-5D02070CB9D4" >
<text x="16" y="81" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebsteilnehmer_Geschäftsfähige_Einheit_FK (Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID)
</text></a>
</g>
<g  fill="rgb(153,255,0)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath21_0_)" transform="translate(1024,1060)" >
<rect x="0" y="0" width="159" height="78" />
<text id="19B5F296-1D5FC327C71A" x="67" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Land
</text>
<line x1="0" y1="17" x2="158" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
U
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
ISO2_Code
</text>
<text x="262" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
VARCHAR2 (2 CHAR)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
ISO3_Code
</text>
<text x="262" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
VARCHAR2 (2 CHAR)
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
ISO_Code_numerisch
</text>
<text x="262" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
VARCHAR2 (2 CHAR)
</text>
<text x="16" y="69" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
TopLevelDomain
</text>
<text x="262" y="69" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="82" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="82" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="82" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
LAND_ID
</text>
<text x="262" y="82" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="152,75 148,67 156,67" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="88" x2="158" y2="88" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="95" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="101" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
LAND_PK (Geografische_Einheit_GEIN_ID, LAND_ID)
</text>
<polygon points="152,75 148,67 156,67" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="107" x2="158" y2="107" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="114" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#4623645A-68B64E30D79B" >
<text x="16" y="120" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Land_Geografische_Einheit_FK (Geografische_Einheit_GEIN_ID)
</text></a>
<polygon points="152,75 148,67 156,67" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(203,218,124)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath11_0_)" transform="translate(456,1393)" >
<rect x="0" y="0" width="282" height="161" />
<text id="38FC9743-5D02070CB9D4" x="79" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Geschäftsfähige_Einheit
</text>
<line x1="0" y1="17" x2="281" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Geschäftsfähige_Einheit_ID
</text>
<text x="288" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Name
</text>
<text x="288" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Kommunikationsmittel_Kommunikationsmittel_ID
</text>
<text x="288" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="62" x2="281" y2="62" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="69" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="75" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Geschäftsfähige_Einheit_PK (Geschäftsfähige_Einheit_ID)
</text>
<line x1="0" y1="81" x2="281" y2="81" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="88" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#4B8B3C74-CEEE2315D8E7" >
<text x="16" y="94" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Geschäftsfähige_Einheit_Kommunikationsmittel_FK (Kommunikationsmittel_Kommunikationsmittel_ID)
</text></a>
<line x1="0" y1="100" x2="281" y2="100" fill="none" stroke="rgb(0,0,255)"/>
<text x="2" y="113" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
U
</text>
<text x="16" y="113" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Geschäftsfähige_Einheit__IDX (Kommunikationsmittel_Kommunikationsmittel_ID)
</text>
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath32_0_)" transform="translate(3311,1021)" >
<rect x="0" y="0" width="160" height="26" />
<text id="8D70D427-FAE524E0B003" x="20" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Qualifizierter_Interessent
</text>
<line x1="0" y1="17" x2="159" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Interessent_Interessent_ID
</text>
<text x="187" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="153,23 149,15 157,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="36" x2="159" y2="36" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="43" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="49" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Qualifizierter_Interessent_PK (Interessent_Interessent_ID)
</text>
<polygon points="153,23 149,15 157,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="55" x2="159" y2="55" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="62" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#C5F5C08D-A2771073ED98" >
<text x="16" y="68" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Qualifizierter_Interessent_Interessent_FK (Interessent_Interessent_ID)
</text></a>
<polygon points="153,23 149,15 157,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath43_0_)" transform="translate(1906,866)" >
<rect x="0" y="0" width="180" height="100" />
<text id="E4C6AAFE-6B5E5EF62F40" x="49" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Vertriebskunde
</text>
<line x1="0" y1="17" x2="179" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebskunde_ID
</text>
<text x="262" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebsteilnehmer_Vertriebsteilnehmer_ID
</text>
<text x="262" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Besitzer_Besitzer_ID
</text>
<text x="262" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="62" x2="179" y2="62" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="69" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="75" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebskunde_PK (Vertriebsteilnehmer_Vertriebsteilnehmer_ID, Vertriebskunde_ID)
</text>
<use xlink:href="#uk_sym" x="4" y="82" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="88" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebskunde_Vertriebskunde_ID_UN (Vertriebskunde_ID)
</text>
<line x1="0" y1="94" x2="179" y2="94" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="101" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#92B0C5FC-140E14D85F0C" >
<text x="16" y="107" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebskunde_Vertriebsteilnehmer_FK (Vertriebsteilnehmer_Vertriebsteilnehmer_ID)
</text></a>
<polygon points="173,97 169,89 177,89" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="113" x2="179" y2="113" fill="none" stroke="rgb(0,0,255)"/>
<text x="2" y="126" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
U
</text>
<text x="16" y="126" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebskunde__IDX (Besitzer_Besitzer_ID)
</text>
<polygon points="173,97 169,89 177,89" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(153,255,0)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath22_0_)" transform="translate(1024,1199)" >
<rect x="0" y="0" width="112" height="52" />
<text id="DA001BC9-C97E68A0C482" x="20" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Ländergruppe
</text>
<line x1="0" y1="17" x2="111" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Typ
</text>
<text x="190" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Zweck
</text>
<text x="190" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="56" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Ländergruppe_ID
</text>
<text x="190" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="105,49 101,41 109,41" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="62" x2="111" y2="62" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="69" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="75" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Ländergruppe_PK (Geografische_Einheit_GEIN_ID, Ländergruppe_ID)
</text>
<polygon points="105,49 101,41 109,41" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="81" x2="111" y2="81" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="88" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#4623645A-68B64E30D79B" >
<text x="16" y="94" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Ländergruppe_Geografische_Einheit_FK (Geografische_Einheit_GEIN_ID)
</text></a>
<polygon points="105,49 101,41 109,41" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath13_0_)" transform="translate(1455,1692)" >
<rect x="0" y="0" width="110" height="27" />
<text id="96CF5C69-9CA5ECFDD8CD" x="34" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Händler
</text>
<line x1="0" y1="17" x2="109" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Handelseinheit_Handelseinheit_ID
</text>
<text x="212" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="103,24 99,16 107,16" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="36" x2="109" y2="36" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="43" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="49" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Händler_PK (Handelseinheit_Handelseinheit_ID)
</text>
<polygon points="103,24 99,16 107,16" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="55" x2="109" y2="55" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="62" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#B730B6D1-784FA44EFCEA" >
<text x="16" y="68" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Händler_Handelseinheit_FK (Handelseinheit_Handelseinheit_ID)
</text></a>
<polygon points="103,24 99,16 107,16" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(203,218,124)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath42_0_)" transform="translate(616,1720)" >
<rect x="0" y="0" width="130" height="67" />
<text id="4A2A6CE7-04C069508D0D" x="43" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Standort
</text>
<line x1="0" y1="17" x2="129" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Name
</text>
<text x="393" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Standort_ID
</text>
<text x="393" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Juristische_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID
</text>
<text x="393" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="69" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Juristische_Person_Juristische_Person_ID
</text>
<text x="393" y="69" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="123,64 119,56 127,56" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="75" x2="129" y2="75" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="82" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="88" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Standort_PK (Standort_ID)
</text>
<polygon points="123,64 119,56 127,56" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="94" x2="129" y2="94" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="101" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#3791AFE5-FA89BDDBAB70" >
<text x="16" y="107" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Standort_Juristische_Person_FK (Juristische_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID, Juristische_Person_Juristische_Person_ID)
</text></a>
<polygon points="123,64 119,56 127,56" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="113" x2="129" y2="113" fill="none" stroke="rgb(0,0,255)"/>
<text x="2" y="126" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
U
</text>
<text x="16" y="126" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Standort__IDX (Kommunikationsmittel_Kommunikationsmittel_ID)
</text>
<polygon points="123,64 119,56 127,56" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(255,255,180)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath37_0_)" transform="translate(1668,1327)" >
<rect x="0" y="0" width="169" height="109" />
<text id="79476DC0-398CC38907C8" x="54" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Relation_53
</text>
<line x1="0" y1="17" x2="168" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Geografische_Einheit_GEIN_ID
</text>
<text x="212" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Handelseinheit_Handelseinheit_ID
</text>
<text x="212" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="49" x2="168" y2="49" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="56" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="62" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_53_PK (Geografische_Einheit_GEIN_ID, Handelseinheit_Handelseinheit_ID)
</text>
<line x1="0" y1="68" x2="168" y2="68" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="75" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#4623645A-68B64E30D79B" >
<text x="16" y="81" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_53_Geografische_Einheit_FK (Geografische_Einheit_GEIN_ID)
</text></a>
<use xlink:href="#fk_sym" x="4" y="88" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#B730B6D1-784FA44EFCEA" >
<text x="16" y="94" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_53_Handelseinheit_FK (Handelseinheit_Handelseinheit_ID)
</text></a>
</g>
<g  fill="rgb(203,218,124)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath27_0_)" transform="translate(1379,1152)" >
<rect x="0" y="0" width="128" height="78" />
<text id="4E447132-09B3FE5665A4" x="46" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
person
</text>
<line x1="0" y1="17" x2="127" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vorname
</text>
<text x="300" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
date_of_birth
</text>
<text x="300" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Geschlecht
</text>
<text x="300" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="69" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="69" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
natürliche_Person_ID
</text>
<text x="300" y="69" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="82" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="82" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="82" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID
</text>
<text x="300" y="82" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="121,75 117,67 125,67" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="88" x2="127" y2="88" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="95" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="101" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
natürliche_Person_PK (Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID, natürliche_Person_ID)
</text>
<polygon points="121,75 117,67 125,67" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="107" x2="127" y2="107" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="114" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#38FC9743-5D02070CB9D4" >
<text x="16" y="120" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
natürliche_Person_Geschäftsfähige_Einheit_FK (Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID)
</text></a>
<polygon points="121,75 117,67 125,67" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath8_0_)" transform="translate(2891,1191)" >
<rect x="0" y="0" width="152" height="26" />
<text id="58D043C6-B1AFF77615FF" x="20" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Finanzierungspartner
</text>
<line x1="0" y1="17" x2="151" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebsteilnehmer_Vertriebsteilnehmer_ID
</text>
<text x="262" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="145,23 141,15 149,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="36" x2="151" y2="36" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="43" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="49" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Finanzierungspartner_PK (Vertriebsteilnehmer_Vertriebsteilnehmer_ID)
</text>
<polygon points="145,23 141,15 149,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="55" x2="151" y2="55" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="62" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#92B0C5FC-140E14D85F0C" >
<text x="16" y="68" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Finanzierungspartner_Vertriebsteilnehmer_FK (Vertriebsteilnehmer_Vertriebsteilnehmer_ID)
</text></a>
<polygon points="145,23 141,15 149,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath41_0_)" transform="translate(2014,2182)" >
<rect x="0" y="0" width="110" height="29" />
<text id="2E47F8A2-D711B5826B42" x="20" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Servicepartner
</text>
<line x1="0" y1="17" x2="109" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Handelseinheit_Handelseinheit_ID
</text>
<text x="212" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
U
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Servicepartner_ID
</text>
<text x="212" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="103,26 99,18 107,18" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="49" x2="109" y2="49" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="56" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="62" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Servicepartner_PK (Handelseinheit_Handelseinheit_ID)
</text>
<polygon points="103,26 99,18 107,18" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="68" x2="109" y2="68" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="75" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#B730B6D1-784FA44EFCEA" >
<text x="16" y="81" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Servicepartner_Handelseinheit_FK (Handelseinheit_Handelseinheit_ID)
</text></a>
<polygon points="103,26 99,18 107,18" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(255,255,180)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath34_0_)" transform="translate(2672,1715)" >
<rect x="0" y="0" width="169" height="112" />
<text id="DFBE6461-8F9498119346" x="51" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Relation_111
</text>
<line x1="0" y1="17" x2="168" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Wettbewerber_Wettbewerber_ID
</text>
<text x="204" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Interessent_Interessent_ID
</text>
<text x="204" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="49" x2="168" y2="49" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="56" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="62" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_111_PK (Wettbewerber_Wettbewerber_ID, Interessent_Interessent_ID)
</text>
<line x1="0" y1="68" x2="168" y2="68" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="75" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#A23A66C0-AA46743F4C07" >
<text x="16" y="81" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_111_Wettbewerber_FK (Wettbewerber_Wettbewerber_ID)
</text></a>
<use xlink:href="#fk_sym" x="4" y="88" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#C5F5C08D-A2771073ED98" >
<text x="16" y="94" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_111_Interessent_FK (Interessent_Interessent_ID)
</text></a>
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath44_0_)" transform="translate(2494,1191)" >
<rect x="0" y="0" width="125" height="50" />
<text id="BB68FE87-4EF1D4AD7ADB" x="20" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Vertriebspartner
</text>
<line x1="0" y1="17" x2="124" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebspartner_ID
</text>
<text x="262" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebsteilnehmer_Vertriebsteilnehmer_ID
</text>
<text x="262" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="49" x2="124" y2="49" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="56" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="62" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebspartner_PK (Vertriebsteilnehmer_Vertriebsteilnehmer_ID, Vertriebspartner_ID)
</text>
<polygon points="118,47 114,39 122,39" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="68" x2="124" y2="68" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="75" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#92B0C5FC-140E14D85F0C" >
<text x="16" y="81" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebspartner_Vertriebsteilnehmer_FK (Vertriebsteilnehmer_Vertriebsteilnehmer_ID)
</text></a>
<polygon points="118,47 114,39 122,39" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(203,218,124)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath28_0_)" transform="translate(20,637)" >
<rect x="0" y="0" width="136" height="63" />
<text id="3408EC76-F74DE9AC1DD8" x="32" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Personenrolle
</text>
<line x1="0" y1="17" x2="135" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Bezeichnung
</text>
<text x="128" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Beschreibung
</text>
<text x="128" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="56" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Personenrolle_ID
</text>
<text x="128" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="62" x2="135" y2="62" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="69" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="75" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Personenrolle_PK (Personenrolle_ID)
</text>
<polygon points="129,60 125,52 133,52" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(255,255,180)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath40_0_)" transform="translate(2589,1302)" >
<rect x="0" y="0" width="169" height="109" />
<text id="EE0AE4E9-E6992ECD752D" x="54" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Relation_62
</text>
<line x1="0" y1="17" x2="168" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebspartner_Vertriebsteilnehmer_Vertriebsteilnehmer_ID
</text>
<text x="348" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebspartner_Vertriebspartner_ID
</text>
<text x="348" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="56" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID
</text>
<text x="348" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="69" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="69" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebskunde_Vertriebskunde_ID
</text>
<text x="348" y="69" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="75" x2="168" y2="75" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="82" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="88" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_62_PK (Vertriebspartner_Vertriebsteilnehmer_Vertriebsteilnehmer_ID, Vertriebspartner_Vertriebspartner_ID, Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID, Vertriebskunde_Vertriebskunde_ID)
</text>
<line x1="0" y1="94" x2="168" y2="94" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="101" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#BB68FE87-4EF1D4AD7ADB" >
<text x="16" y="107" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_62_Vertriebspartner_FK (Vertriebspartner_Vertriebsteilnehmer_Vertriebsteilnehmer_ID, Vertriebspartner_Vertriebspartner_ID)
</text></a>
<use xlink:href="#fk_sym" x="4" y="114" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#E4C6AAFE-6B5E5EF62F40" >
<text x="16" y="120" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_62_Vertriebskunde_FK (Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID, Vertriebskunde_Vertriebskunde_ID)
</text></a>
<polygon points="162,106 158,98 166,98" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(203,218,124)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath14_0_)" transform="translate(1503,1004)" >
<rect x="0" y="0" width="136" height="63" />
<text id="F8C5905E-281E392B3111" x="45" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Haushalt
</text>
<line x1="0" y1="17" x2="135" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Haushalt_ID
</text>
<text x="104" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="36" x2="135" y2="36" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="43" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="49" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Haushalt_PK (Haushalt_ID)
</text>
</g>
<g  fill="rgb(153,255,0)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath29_0_)" transform="translate(1023,752)" >
<rect x="0" y="0" width="142" height="52" />
<text id="C0B4ACF6-15D198ED9BD8" x="43" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
PLZ-Gebiet
</text>
<line x1="0" y1="17" x2="141" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Postleitzahl
</text>
<text x="227" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
PLZ-Ebene
</text>
<text x="227" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="56" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
PLZ-Gebiet_ID
</text>
<text x="227" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="135,49 131,41 139,41" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="62" x2="141" y2="62" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="69" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="75" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
PLZ-Gebiet_PK (Gebiet_Geografische_Einheit_GEIN_ID, PLZ-Gebiet_ID)
</text>
<polygon points="135,49 131,41 139,41" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="81" x2="141" y2="81" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="88" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#616FBC25-5093773E214A" >
<text x="16" y="94" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
PLZ-Gebiet_Gebiet_FK (Gebiet_Geografische_Einheit_GEIN_ID)
</text></a>
<polygon points="135,49 131,41 139,41" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(255,255,180)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath35_0_)" transform="translate(20,467)" >
<rect x="0" y="0" width="169" height="109" />
<text id="287C0437-6D84B613815E" x="54" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Relation_46
</text>
<line x1="0" y1="17" x2="168" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Ansprechpartner_Ansprechpartner_ID
</text>
<text x="228" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Personenrolle_Personenrolle_ID
</text>
<text x="228" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="49" x2="168" y2="49" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="56" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="62" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_46_PK (Ansprechpartner_Ansprechpartner_ID, Personenrolle_Personenrolle_ID)
</text>
<line x1="0" y1="68" x2="168" y2="68" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="75" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#FA90040D-641F12C234A3" >
<text x="16" y="81" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_46_Ansprechpartner_FK (Ansprechpartner_Ansprechpartner_ID)
</text></a>
<use xlink:href="#fk_sym" x="4" y="88" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#3408EC76-F74DE9AC1DD8" >
<text x="16" y="94" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_46_Personenrolle_FK (Personenrolle_Personenrolle_ID)
</text></a>
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath25_0_)" transform="translate(3124,1191)" >
<rect x="0" y="0" width="72" height="26" />
<text id="2E510FC7-A21C3CA81706" x="20" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Nutzer
</text>
<line x1="0" y1="17" x2="71" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebsteilnehmer_Vertriebsteilnehmer_ID
</text>
<text x="262" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="65,23 61,15 69,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="36" x2="71" y2="36" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="43" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="49" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Nutzer_PK (Vertriebsteilnehmer_Vertriebsteilnehmer_ID)
</text>
<polygon points="65,23 61,15 69,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="55" x2="71" y2="55" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="62" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#92B0C5FC-140E14D85F0C" >
<text x="16" y="68" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Nutzer_Vertriebsteilnehmer_FK (Vertriebsteilnehmer_Vertriebsteilnehmer_ID)
</text></a>
<polygon points="65,23 61,15 69,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath23_0_)" transform="translate(1863,1352)" >
<rect x="0" y="0" width="118" height="26" />
<text id="BA02059E-B07A74E4D45C" x="20" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Leasingnehmer
</text>
<line x1="0" y1="17" x2="117" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID
</text>
<text x="342" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="111,23 107,15 115,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="36" x2="117" y2="36" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="43" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="49" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Leasingnehmer_PK (Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID)
</text>
<polygon points="111,23 107,15 115,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="55" x2="117" y2="55" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="62" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#E4C6AAFE-6B5E5EF62F40" >
<text x="16" y="68" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Leasingnehmer_Vertriebskunde_FK (Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID)
</text></a>
<polygon points="111,23 107,15 115,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(203,218,124)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath18_0_)" transform="translate(857,1637)" >
<rect x="0" y="0" width="131" height="83" />
<text id="3791AFE5-FA89BDDBAB70" x="20" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Juristische_Person
</text>
<line x1="0" y1="17" x2="130" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Gesellschaftsform
</text>
<text x="300" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
UID_Nr
</text>
<text x="300" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="56" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Juristische_Person_ID
</text>
<text x="300" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="69" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="69" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID
</text>
<text x="300" y="69" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="75" x2="130" y2="75" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="82" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="88" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Juristische_Person_PK (Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID, Juristische_Person_ID)
</text>
<polygon points="124,80 120,72 128,72" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="94" x2="130" y2="94" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="101" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#38FC9743-5D02070CB9D4" >
<text x="16" y="107" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Juristische_Person_Geschäftsfähige_Einheit_FK (Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID)
</text></a>
<polygon points="124,80 120,72 128,72" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath6_0_)" transform="translate(2891,1278)" >
<rect x="0" y="0" width="110" height="59" />
<text id="5F5A46F2-0F0F43ECD471" x="25" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Eigentümer
</text>
<line x1="0" y1="17" x2="109" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Eigentümer_ID
</text>
<text x="380" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="2" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Finanzierungspartner_Vertriebsteilnehmer_Vertriebsteilnehmer_ID
</text>
<text x="380" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="2" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebspartner_Vertriebsteilnehmer_Vertriebsteilnehmer_ID
</text>
<text x="380" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="69" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="2" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Käufer_Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID
</text>
<text x="380" y="69" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="103,56 99,48 107,48" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="75" x2="109" y2="75" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="82" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="88" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Eigentümer_PK (Eigentümer_ID)
</text>
<polygon points="103,56 99,48 107,48" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="94" x2="109" y2="94" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="101" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#58D043C6-B1AFF77615FF" >
<text x="16" y="107" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Eigentümer_Finanzierungspartner_FK (Finanzierungspartner_Vertriebsteilnehmer_Vertriebsteilnehmer_ID)
</text></a>
<polygon points="103,56 99,48 107,48" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="113" x2="109" y2="113" fill="none" stroke="rgb(0,0,255)"/>
<text x="2" y="126" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
U
</text>
<text x="16" y="126" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Eigentümer__IDX (Finanzierungspartner_Vertriebsteilnehmer_Vertriebsteilnehmer_ID)
</text>
<polygon points="103,56 99,48 107,48" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath7_0_)" transform="translate(1264,1692)" >
<rect x="0" y="0" width="110" height="27" />
<text id="9CAA3C40-90F379DD2F0B" x="40" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Filiale
</text>
<line x1="0" y1="17" x2="109" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Handelseinheit_Handelseinheit_ID
</text>
<text x="212" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="103,24 99,16 107,16" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="36" x2="109" y2="36" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="43" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="49" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Filiale_PK (Handelseinheit_Handelseinheit_ID)
</text>
<polygon points="103,24 99,16 107,16" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="55" x2="109" y2="55" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="62" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#B730B6D1-784FA44EFCEA" >
<text x="16" y="68" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Filiale_Handelseinheit_FK (Handelseinheit_Handelseinheit_ID)
</text></a>
<polygon points="103,24 99,16 107,16" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(153,255,0)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath10_0_)" transform="translate(1333,284)" >
<rect x="0" y="0" width="357" height="370" />
<text id="4623645A-68B64E30D79B" x="124" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Geografische_Einheit
</text>
<line x1="0" y1="17" x2="356" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
GEIN_ID
</text>
<text x="122" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Name_[L]
</text>
<text x="122" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
VARCHAR2 (60)
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
GeoInformation
</text>
<text x="122" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<line x1="0" y1="62" x2="356" y2="62" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="69" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="75" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
GEIN_PK (GEIN_ID)
</text>
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath5_0_)" transform="translate(2398,1302)" >
<rect x="0" y="0" width="110" height="59" />
<text id="ED3FC77A-C8FAB0739751" x="34" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Besitzer
</text>
<line x1="0" y1="17" x2="109" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Besitzer_ID
</text>
<text x="348" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="2" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID
</text>
<text x="348" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="2" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebskunde_Vertriebskunde_ID
</text>
<text x="348" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="69" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="2" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebspartner_Vertriebsteilnehmer_Vertriebsteilnehmer_ID
</text>
<text x="348" y="69" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="103,56 99,48 107,48" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="75" x2="109" y2="75" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="82" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="88" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Besitzer_PK (Besitzer_ID)
</text>
<polygon points="103,56 99,48 107,48" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="94" x2="109" y2="94" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="101" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#E4C6AAFE-6B5E5EF62F40" >
<text x="16" y="107" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Besitzer_Vertriebskunde_FK (Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID, Vertriebskunde_Vertriebskunde_ID)
</text></a>
<polygon points="103,56 99,48 107,48" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="113" x2="109" y2="113" fill="none" stroke="rgb(0,0,255)"/>
<text x="2" y="126" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
U
</text>
<text x="16" y="126" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Besitzer__IDX (Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID, Vertriebskunde_Vertriebskunde_ID)
</text>
<polygon points="103,56 99,48 107,48" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(203,218,124)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath26_0_)" transform="translate(583,330)" >
<rect x="0" y="0" width="136" height="63" />
<text id="C0BF57A2-DC6F635193E1" x="20" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Organisationseinheit
</text>
<line x1="0" y1="17" x2="135" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Name
</text>
<text x="393" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Organisationseinheit_ID
</text>
<text x="393" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
bild1v6v1_bild1v6v1_ID
</text>
<text x="393" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="69" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Juristische_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID
</text>
<text x="393" y="69" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="129,60 125,52 133,52" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="75" x2="135" y2="75" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="82" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="88" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Organisationseinheit_PK (Organisationseinheit_ID)
</text>
<polygon points="129,60 125,52 133,52" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="94" x2="135" y2="94" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="101" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#3791AFE5-FA89BDDBAB70" >
<text x="16" y="107" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Organisationseinheit_Juristische_Person_FK (Juristische_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID, Juristische_Person_Juristische_Person_ID)
</text></a>
<polygon points="129,60 125,52 133,52" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="113" x2="135" y2="113" fill="none" stroke="rgb(0,0,255)"/>
<text x="2" y="126" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
U
</text>
<text x="16" y="126" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Organisationseinheit__IDX (bild1v6v1_bild1v6v1_ID)
</text>
<polygon points="129,60 125,52 133,52" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath24_0_)" transform="translate(2062,1352)" >
<rect x="0" y="0" width="69" height="26" />
<text id="5982D485-4B124D297779" x="20" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Mieter
</text>
<line x1="0" y1="17" x2="68" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID
</text>
<text x="342" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="62,23 58,15 66,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="36" x2="68" y2="36" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="43" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="49" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Mieter_PK (Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID)
</text>
<polygon points="62,23 58,15 66,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="55" x2="68" y2="55" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="62" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#E4C6AAFE-6B5E5EF62F40" >
<text x="16" y="68" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Mieter_Vertriebskunde_FK (Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID)
</text></a>
<polygon points="62,23 58,15 66,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath12_0_)" transform="translate(1908,1830)" >
<rect x="0" y="0" width="270" height="193" />
<text id="B730B6D1-784FA44EFCEA" x="96" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Handelseinheit
</text>
<line x1="0" y1="17" x2="269" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Handelseinheit_ID
</text>
<text x="348" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Professionalisierungsgrad
</text>
<text x="348" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="2" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebspartner_Vertriebsteilnehmer_Vertriebsteilnehmer_ID
</text>
<text x="348" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="69" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="2" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebspartner_Vertriebspartner_ID
</text>
<text x="348" y="69" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="82" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="2" y="82" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="82" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Wettbewerber_Wettbewerber_ID
</text>
<text x="348" y="82" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="88" x2="269" y2="88" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="95" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="101" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Handelseinheit_PK (Handelseinheit_ID)
</text>
<line x1="0" y1="107" x2="269" y2="107" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="114" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#BB68FE87-4EF1D4AD7ADB" >
<text x="16" y="120" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Handelseinheit_Vertriebspartner_FK (Vertriebspartner_Vertriebsteilnehmer_Vertriebsteilnehmer_ID, Vertriebspartner_Vertriebspartner_ID)
</text></a>
<use xlink:href="#fk_sym" x="4" y="127" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#A23A66C0-AA46743F4C07" >
<text x="16" y="133" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Handelseinheit_Wettbewerber_FK (Wettbewerber_Wettbewerber_ID)
</text></a>
</g>
<g  fill="rgb(255,255,180)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath36_0_)" transform="translate(2148,1191)" >
<rect x="0" y="0" width="169" height="109" />
<text id="483BA939-CB0BAFFB304C" x="54" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Relation_48
</text>
<line x1="0" y1="17" x2="168" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Handelseinheit_Handelseinheit_ID
</text>
<text x="262" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebsteilnehmer_Vertriebsteilnehmer_ID
</text>
<text x="262" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="49" x2="168" y2="49" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="56" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="62" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_48_PK (Handelseinheit_Handelseinheit_ID, Vertriebsteilnehmer_Vertriebsteilnehmer_ID)
</text>
<line x1="0" y1="68" x2="168" y2="68" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="75" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#B730B6D1-784FA44EFCEA" >
<text x="16" y="81" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_48_Handelseinheit_FK (Handelseinheit_Handelseinheit_ID)
</text></a>
<use xlink:href="#fk_sym" x="4" y="88" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#92B0C5FC-140E14D85F0C" >
<text x="16" y="94" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_48_Vertriebsteilnehmer_FK (Vertriebsteilnehmer_Vertriebsteilnehmer_ID)
</text></a>
</g>
<g  fill="rgb(153,255,0)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath9_0_)" transform="translate(1023,865)" >
<rect x="0" y="0" width="190" height="134" />
<text id="616FBC25-5093773E214A" x="79" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Gebiet
</text>
<line x1="0" y1="17" x2="189" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Geografische_Einheit_GEIN_ID
</text>
<text x="227" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
U
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Gebiet_ID
</text>
<text x="227" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Land_Geografische_Einheit_GEIN_ID
</text>
<text x="227" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="69" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Land_LAND_ID
</text>
<text x="227" y="69" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="82" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="2" y="82" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="82" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Gebiet_Geografische_Einheit_GEIN_ID
</text>
<text x="227" y="82" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="88" x2="189" y2="88" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="95" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="101" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Gebiet_PK (Geografische_Einheit_GEIN_ID)
</text>
<use xlink:href="#uk_sym" x="4" y="108" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="114" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Gebiet_Gebiet_ID_UN (Gebiet_ID)
</text>
<line x1="0" y1="120" x2="189" y2="120" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="127" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#4623645A-68B64E30D79B" >
<text x="16" y="133" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Gebiet_Geografische_Einheit_FK (Geografische_Einheit_GEIN_ID)
</text></a>
<use xlink:href="#fk_sym" x="4" y="140" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#19B5F296-1D5FC327C71A" >
<text x="16" y="146" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Gebiet_Land_FK (Land_Geografische_Einheit_GEIN_ID, Land_LAND_ID)
</text></a>
<polygon points="183,131 179,123 187,123" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath3_0_)" transform="translate(1857,1670)" >
<rect x="0" y="0" width="110" height="26" />
<text id="6FE73FE2-D227280DE9FD" x="40" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Agent
</text>
<line x1="0" y1="17" x2="109" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Handelseinheit_Handelseinheit_ID
</text>
<text x="212" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="103,23 99,15 107,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="36" x2="109" y2="36" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="43" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="49" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Agent_PK (Handelseinheit_Handelseinheit_ID)
</text>
<polygon points="103,23 99,15 107,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="55" x2="109" y2="55" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="62" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#B730B6D1-784FA44EFCEA" >
<text x="16" y="68" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Agent_Handelseinheit_FK (Handelseinheit_Handelseinheit_ID)
</text></a>
<polygon points="103,23 99,15 107,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(153,255,0)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath1_0_)" transform="translate(800,1060)" >
<rect x="0" y="0" width="142" height="52" />
<text id="A9178943-A6B967DF23BB" x="20" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Administrativgebiet
</text>
<line x1="0" y1="17" x2="141" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Gebiet_Geografische_Einheit_GEIN_ID
</text>
<text x="227" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Administrativebene
</text>
<text x="227" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="56" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
U
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Administrativgebiet_ID
</text>
<text x="227" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="135,49 131,41 139,41" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="62" x2="141" y2="62" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="69" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="75" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Administrativgebiet_PK (Gebiet_Geografische_Einheit_GEIN_ID)
</text>
<polygon points="135,49 131,41 139,41" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="81" x2="141" y2="81" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="88" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#616FBC25-5093773E214A" >
<text x="16" y="94" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Administrativgebiet_Gebiet_FK (Gebiet_Geografische_Einheit_GEIN_ID)
</text></a>
<polygon points="135,49 131,41 139,41" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(203,218,124)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath20_0_)" transform="translate(339,1985)" >
<rect x="0" y="0" width="146" height="80" />
<text id="4B8B3C74-CEEE2315D8E7" x="20" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Kommunikationsmittel
</text>
<line x1="0" y1="17" x2="145" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
eMail
</text>
<text x="300" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Fixnet_Tel_Nr
</text>
<text x="300" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Mobil_Tel_Nr
</text>
<text x="300" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="69" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="26" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Webseite
</text>
<text x="300" y="69" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="82" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="82" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="82" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Kommunikationsmittel_ID
</text>
<text x="300" y="82" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="139,77 135,69 143,69" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="88" x2="145" y2="88" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="95" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="101" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Kommunikationsmittel_PK (Kommunikationsmittel_ID)
</text>
<polygon points="139,77 135,69 143,69" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="107" x2="145" y2="107" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="114" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#38FC9743-5D02070CB9D4" >
<text x="16" y="120" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Kommunikationsmittel_Geschäftsfähige_Einheit_FK (Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID)
</text></a>
<polygon points="139,77 135,69 143,69" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="126" x2="145" y2="126" fill="none" stroke="rgb(0,0,255)"/>
<text x="2" y="139" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
U
</text>
<text x="16" y="139" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Kommunikationsmittel__IDX (Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID)
</text>
<polygon points="139,77 135,69 143,69" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(255,153,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath31_0_)" transform="translate(2700,1398)" >
<rect x="0" y="0" width="110" height="59" />
<text id="034D5BEE-DE0D3271FD40" x="20" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Produktinstanz
</text>
<line x1="0" y1="17" x2="109" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Serie-Nr
</text>
<text x="176" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
UNKNOWN
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Produktinstanz_ID
</text>
<text x="176" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="56" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="2" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="56" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Besitzer_Besitzer_ID
</text>
<text x="176" y="56" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="69" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">

</text>
<text x="2" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="69" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Eigentümer_Eigentümer_ID
</text>
<text x="176" y="69" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="103,56 99,48 107,48" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="75" x2="109" y2="75" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="82" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="88" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Produktinstanz_PK (Produktinstanz_ID)
</text>
<polygon points="103,56 99,48 107,48" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="94" x2="109" y2="94" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="101" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#ED3FC77A-C8FAB0739751" >
<text x="16" y="107" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Produktinstanz_Besitzer_FK (Besitzer_Besitzer_ID)
</text></a>
<polygon points="103,56 99,48 107,48" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath30_0_)" transform="translate(3070,1021)" >
<rect x="0" y="0" width="160" height="26" />
<text id="9D6529BD-EBCDFDECA13C" x="20" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Potenzieller_Interessent
</text>
<line x1="0" y1="17" x2="159" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Interessent_Interessent_ID
</text>
<text x="180" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="153,23 149,15 157,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="36" x2="159" y2="36" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="43" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="49" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Potenzieller_Interessent_PK (Interessent_Interessent_ID)
</text>
<polygon points="153,23 149,15 157,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="55" x2="159" y2="55" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="62" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#C5F5C08D-A2771073ED98" >
<text x="16" y="68" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Potenzieller_Interessent_Interessent_FK (Interessent_Interessent_ID)
</text></a>
<polygon points="153,23 149,15 157,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath15_0_)" transform="translate(1646,1692)" >
<rect x="0" y="0" width="110" height="27" />
<text id="34FFB858-9CFAD1016B23" x="29" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Importeur
</text>
<line x1="0" y1="17" x2="109" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Handelseinheit_Handelseinheit_ID
</text>
<text x="212" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="103,24 99,16 107,16" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="36" x2="109" y2="36" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="43" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="49" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Importeur_PK (Handelseinheit_Handelseinheit_ID)
</text>
<polygon points="103,24 99,16 107,16" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="55" x2="109" y2="55" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="62" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#B730B6D1-784FA44EFCEA" >
<text x="16" y="68" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Importeur_Handelseinheit_FK (Handelseinheit_Handelseinheit_ID)
</text></a>
<polygon points="103,24 99,16 107,16" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath16_0_)" transform="translate(1823,2182)" >
<rect x="0" y="0" width="110" height="29" />
<text id="F34E49B6-8FFE27D65CDE" x="25" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Installateur
</text>
<line x1="0" y1="17" x2="109" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Handelseinheit_Handelseinheit_ID
</text>
<text x="212" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
U
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Installateur_ID
</text>
<text x="212" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="103,26 99,18 107,18" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="49" x2="109" y2="49" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="56" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="62" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Installateur_PK (Handelseinheit_Handelseinheit_ID)
</text>
<polygon points="103,26 99,18 107,18" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="68" x2="109" y2="68" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="75" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#B730B6D1-784FA44EFCEA" >
<text x="16" y="81" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Installateur_Handelseinheit_FK (Handelseinheit_Handelseinheit_ID)
</text></a>
<polygon points="103,26 99,18 107,18" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath19_0_)" transform="translate(2235,985)" >
<rect x="0" y="0" width="71" height="26" />
<text id="C297FED9-D4C3114CB153" x="20" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Käufer
</text>
<line x1="0" y1="17" x2="70" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID
</text>
<text x="342" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<polygon points="64,23 60,15 68,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="36" x2="70" y2="36" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="43" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="49" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Käufer_PK (Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID)
</text>
<polygon points="64,23 60,15 68,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="55" x2="70" y2="55" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="62" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#E4C6AAFE-6B5E5EF62F40" >
<text x="16" y="68" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Käufer_Vertriebskunde_FK (Vertriebskunde_Vertriebsteilnehmer_Vertriebsteilnehmer_ID)
</text></a>
<polygon points="64,23 60,15 68,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
<line x1="0" y1="74" x2="70" y2="74" fill="none" stroke="rgb(0,0,255)"/>
<text x="2" y="87" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
U
</text>
<text x="16" y="87" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Käufer__IDX (Eigentümer_Eigentümer_ID)
</text>
<polygon points="64,23 60,15 68,15" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath46_0_)" transform="translate(2497,1584)" >
<rect x="0" y="0" width="110" height="73" />
<text id="A23A66C0-AA46743F4C07" x="20" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Wettbewerber
</text>
<line x1="0" y1="17" x2="109" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Wettbewerber_ID
</text>
<text x="300" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID
</text>
<text x="300" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="49" x2="109" y2="49" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="56" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="62" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Wettbewerber_PK (Wettbewerber_ID)
</text>
<line x1="0" y1="68" x2="109" y2="68" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="75" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#38FC9743-5D02070CB9D4" >
<text x="16" y="81" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Wettbewerber_Geschäftsfähige_Einheit_FK (Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID)
</text></a>
<polygon points="103,70 99,62 107,62" stroke-dasharray="none" stroke="rgb(0,0,255)" fill="rgb(0,0,255)" stroke-width="1" />
</g>
<g  fill="rgb(0,204,255)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath17_0_)" transform="translate(3191,865)" >
<rect x="0" y="0" width="191" height="95" />
<text id="C5F5C08D-A2771073ED98" x="66" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Interessent
</text>
<line x1="0" y1="17" x2="190" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
P
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Interessent_ID
</text>
<text x="300" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
F
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID
</text>
<text x="300" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="49" x2="190" y2="49" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="56" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="62" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Interessent_PK (Interessent_ID)
</text>
<line x1="0" y1="68" x2="190" y2="68" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="75" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#38FC9743-5D02070CB9D4" >
<text x="16" y="81" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Interessent_Geschäftsfähige_Einheit_FK (Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID)
</text></a>
</g>
<g  fill="rgb(255,255,180)" stroke="rgb(0,0,255)" fill-opacity="1.0" stroke-opacity="1.0" clip-path="url(#clipPath33_0_)" transform="translate(1078,1566)" >
<rect x="0" y="0" width="169" height="113" />
<text id="4F452D3C-CF2EAD28C059" x="58" y="13" fill="rgb(0,0,255)" font-weight="bold"  fill-opacity="1.0" font-size="10" stroke="none">
Relation_1
</text>
<line x1="0" y1="17" x2="168" y2="17" fill="none" stroke="rgb(0,0,255)"/>
<text x="16" y="30" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="30" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="30" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Juristische_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID
</text>
<text x="399" y="30" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<text x="16" y="43" fill="rgb(255,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
*
</text>
<text x="2" y="43" fill="rgb(0,0,255)" fill-opacity="1.0" font-size="10" stroke="none">
PF
</text>
<text x="26" y="43" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Juristische_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID1
</text>
<text x="399" y="43" fill="rgb(0,128,0)" fill-opacity="1.0" font-size="10" stroke="none">
NUMBER (10)
</text>
<line x1="0" y1="49" x2="168" y2="49" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#pk_sym" x="4" y="56" width="8" height="8" fill-opacity="1.0"/>
<text x="16" y="62" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_1_PK (Juristische_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID, Juristische_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID1)
</text>
<line x1="0" y1="68" x2="168" y2="68" fill="none" stroke="rgb(0,0,255)"/>
<use xlink:href="#fk_sym" x="4" y="75" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#3791AFE5-FA89BDDBAB70" >
<text x="16" y="81" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_1_Juristische_Person_FK (Juristische_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID)
</text></a>
<use xlink:href="#fk_sym" x="4" y="88" width="8" height="8" fill-opacity="1.0"/><a xlink:href="#3791AFE5-FA89BDDBAB70" >
<text x="16" y="94" fill="rgb(0,0,0)" fill-opacity="1.0" font-size="10" stroke="none">
Relation_1_Juristische_Person_FKv1 (Juristische_Person_Geschäftsfähige_Einheit_Geschäftsfähige_Einheit_ID1)
</text></a>
</g>
<g fill="none" stroke="rgb(0,0,0)" transform="translate(1003.0,845.0)" >
<circle stroke-dasharray="none" cx="90.0" cy="2.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="2.0" cy="156.60550458715602" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<path d=" M13.0 177.60553 C 13.0 177.60553 3.0 177.60553 3.0 167.60553 L3.0 14.0 C 3.0 14.0 3.0 3.0 17.0 3.0 L101.0 3.0 C 101.0 3.0 111.0 3.0 111.0 13.0"/>
</g>
<g fill="none" stroke="rgb(0,0,0)" transform="translate(1888.0,1810.0)" >
<circle stroke-dasharray="none" cx="236.2874149659865" cy="2.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="306.0" cy="24.389937106918296" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<path d=" M217.28735 13.0 C 217.28735 13.0 217.28735 3.0 227.28735 3.0 L293.0 3.0 C 293.0 3.0 307.0 3.0 307.0 17.0 L307.0 35.389893 C 307.0 35.389893 307.0 45.389893 297.0 45.389893"/>
</g>
<g fill="none" stroke="rgb(0,0,0)" transform="translate(2378.0,1282.0)" >
<circle stroke-dasharray="none" cx="36.56417910447772" cy="2.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="122.0" cy="2.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<path d=" M17.564209 13.0 C 17.564209 13.0 17.564209 3.0 27.564209 3.0 L133.0 3.0 C 133.0 3.0 143.0 3.0 143.0 13.0"/>
</g>
<g fill="none" stroke="rgb(0,0,0)" transform="translate(3171.0,845.0)" >
<circle stroke-dasharray="none" cx="39.0" cy="131.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="175.0" cy="131.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<path d=" M196.0 122.0 C 196.0 122.0 196.0 132.0 186.0 132.0 L30.0 132.0 C 30.0 132.0 20.0 132.0 20.0 122.0"/>
</g>
<g fill="none" stroke="rgb(0,0,0)" transform="translate(1886.0,846.0)" >
<circle stroke-dasharray="none" cx="187.0" cy="136.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="216.0" cy="100.75675675675677" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="57.0" cy="136.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<path d=" M207.0 81.756775 C 207.0 81.756775 217.0 81.756775 217.0 91.756775 L217.0 123.0 C 217.0 123.0 217.0 137.0 203.0 137.0 L48.0 137.0 C 48.0 137.0 38.0 137.0 38.0 127.0"/>
</g>
<g fill="none" stroke="rgb(0,0,0)" transform="translate(2871.0,1258.0)" >
<circle stroke-dasharray="none" cx="2.0" cy="31.047970479704873" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="2.0" cy="4.953795379537951" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="74.0" cy="2.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<path d=" M13.0 52.047974 C 13.0 52.047974 3.0 52.047974 3.0 42.047974 L3.0 14.0 C 3.0 14.0 3.0 3.0 17.0 3.0 L85.0 3.0 C 85.0 3.0 95.0 3.0 95.0 13.0"/>
</g>
<g fill="none" stroke="rgb(0,0,0)" transform="translate(1313.0,264.0)" >
<circle stroke-dasharray="none" cx="26.361904761904725" cy="406.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="82.8529411764705" cy="406.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="66.64938271604933" cy="406.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<path d=" M103.852905 397.0 C 103.852905 397.0 103.852905 407.0 93.852905 407.0 L17.361938 407.0 C 17.361938 407.0 7.3619385 407.0 7.3619385 397.0"/>
</g>
<g fill="none" stroke="rgb(0,0,0)" transform="translate(2629.0,845.0)" >
<circle stroke-dasharray="none" cx="310.0" cy="301.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="2.0" cy="70.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="9.800000000000182" cy="301.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="376.0" cy="264.7297297297298" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<path d=" M367.0 245.72974 C 367.0 245.72974 377.0 245.72974 377.0 255.72974 L377.0 288.0 C 377.0 288.0 377.0 302.0 363.0 302.0 L17.0 302.0 C 14.0 302.0 3.0 302.0 3.0 288.0 L3.0 61.0 C 3.0 61.0 3.0 51.0 13.0 51.0"/>
</g>
<g fill="none" stroke="rgb(0,0,0)" transform="translate(436.0,1373.0)" >
<circle stroke-dasharray="none" cx="314.56097560975604" cy="197.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="318.0" cy="46.674999999999955" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<path d=" M309.0 27.675049 C 309.0 27.675049 319.0 27.675049 319.0 37.67505 L319.0 184.0 C 319.0 184.0 319.0 198.0 305.0 198.0 L305.56097 198.0 C 305.56097 198.0 295.56097 198.0 295.56097 188.0"/>
</g>
<g fill="none" stroke="rgb(0,0,0)" transform="translate(1868.0,1790.0)" >
<circle stroke-dasharray="none" cx="52.0" cy="269.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="2.0" cy="63.75274725274721" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="200.0" cy="269.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="69.0" cy="2.0" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="2.0" cy="24.200000000000045" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<circle stroke-dasharray="none" cx="2.0" cy="82.75690607734805" stroke="rgb(0,0,0)" r="2" fill="rgb(0,0,0)" stroke-width="1" />
<path d=" M221.0 260.0 C 221.0 260.0 221.0 270.0 211.0 270.0 L17.0 270.0 C 17.0 270.0 3.0 270.0 3.0 256.0 L3.0 17.0 C 3.0 17.0 3.0 3.0 17.0 3.0 L80.0 3.0 C 80.0 3.0 90.0 3.0 90.0 13.0"/>
</g>

</svg>""")
print (m[1],m[2])
